# util
from django.shortcuts import get_object_or_404
from concurrent.futures import ThreadPoolExecutor
from django.db.models import Q

# service
from apps.commons.services import service_bookInfo as si
from apps.commons.services import service_series   as ss
from apps.commons.services import service_author   as sa
from apps.commons.services import service_genrue   as sg
from apps.commons.services import service_book     as sb

# common
from apps.commons.util import utils
from apps.commons.bookutil import book_util
from apps.commons.const import appconst

# db
from apps.book.models import Workbook

"""
Book
"""
# 初期表示
def retriveWorkbooks(text, 
                     nonecheck = None, 
                     newcheck = None, 
                     delcheck = None, 
                     createcheck = None):
    check = Q()
    search = Q()

    if text:
        search.add(Q(name__icontains = text), Q.AND)

    if nonecheck or newcheck or delcheck or createcheck:
        if nonecheck:
            check.add(Q(process = 'None'), Q.OR)
        if newcheck:
            check.add(Q(process = 'Edit'), Q.OR)
        if delcheck:
            check.add(Q(process = 'Delete'), Q.OR)
        if createcheck:
            check.add(Q(process = 'Create'), Q.OR)
    search.add(check, Q.AND)

    return Workbook.objects.filter(search).order_by('name', 'book_name')
# workbook最新化
def getLatestList():
    # 空フォルダの削除
    utils.folderEmptyDelete(appconst.FOLDER_TORRENT)
    # 書籍ファイルの取得
    file_folder = []
    for book in utils.getFiles(appconst.FOLDER_TORRENT, appconst.EXTENTION_BOOK):
        file_folder.append(book)
    # 書籍フォルダの取得
    for folder in utils.getFolders(appconst.FOLDER_TORRENT, appconst.EXTENTION_IMAGE):
        file_folder.append(folder)
    
    # 存在しないデータは削除
    for wb in Workbook.objects.all():
        if wb.path not in file_folder:
            wb.delete()
    # 最新化    
    for item in file_folder:
        name = utils.getFileName(item)
        print(name)
        wb = Workbook.objects.filter(path__exact=item)
        if not wb:
            # 登録
            Workbook.objects.get_or_create(
                process     = 'None',
                path        = item,
                name        = name,
                genrue_id   = 0,
                genrue_name = '',
                story_by_id = 0,
                story_by    = '',
                art_by_id   = 0,
                art_by      = '',
                book_id     = 0,
                title       = '',
                sub_title   = '',
                volume      = 0,
                book_name   = '',
                save_path   = '',
                exist_flg   = False,
            )
# 書籍名設定
def settting():
    workbooks = Workbook.objects.all()
    for item in workbooks:
        print(item.name)
        name = item.name
        extention = utils.getExtention(item.path)
        if not extention:
            extention = '.pdf'

        genrue_id = book_util.get_genrue_id(name)
        
        # 更新
        (genrue_id, title, sub_title, process) = book_util.get_title(genrue_id, name)
        name = name.replace(title, '')
        name = name.replace(sub_title, '')

        genrue_name = book_util.get_genrue_name(genrue_id)
        name = name.replace(genrue_name, '')

        story_by = book_util.get_author(name)
        name = name.replace(story_by, '')

        art_by = book_util.get_author(name).replace('×', '')
        name = name.replace(art_by, '')
        
        volume = utils.getVolume(name, appconst.REGEX_VOLUME)
        
        book_name = book_util.get_book_name(genrue_name, story_by, art_by, title, sub_title, volume)
        save_path = book_util.get_save_path(genrue_id) + book_name + extention

        item.process = process
        item.genrue_id = genrue_id
        item.genrue_name = genrue_name.strip()
        item.title = title.strip()
        item.sub_title = sub_title.strip()
        item.story_by = story_by.strip()
        item.story_by_id = book_util.get_author_id(genrue_id, story_by.strip())
        item.art_by = art_by.strip()
        item.art_by_id = book_util.get_author_id(genrue_id, art_by)
        item.volume = volume
        item.book_name = book_name.strip()
        item.save_path = save_path.strip()
        item.exist_flg = utils.existFile(save_path)
        item.book_id = book_util.get_book_id(genrue_id, story_by, art_by, title, sub_title)
        item.save()
# 置換
def replace(before, after, isRegex):
    if isRegex:
        for wb in Workbook.objects.all():
            wb.name = utils.replace(wb.name, before, after)
            wb.save()
    else:
        for wb in Workbook.objects.filter(name__icontains = before):
            wb.name = wb.name.replace(before, after)
            wb.save()
# 処理変更
def process(id, process):
    wb = Workbook.objects.get(pk=id)
    wb.process = process
    wb.save()
# workbook取得
def getWorkbook(pk):
    return get_object_or_404(Workbook, pk=pk)
# pdfパスの取得
def getPDFpath(name):
    if not name:
        path = appconst.TORRENT_URL + name
    else:
        path = None
    return path
# 次へ
def next(id):
    name = Workbook.objects.get(pk=id).name
    next = Workbook.objects.filter(~Q(process='Create'),~Q(process='Delete'),name__gt=name).order_by('name','volume').first().id
    return next
# 実行
def execute():
    errMsg = []
    tpe = ThreadPoolExecutor(max_workers=10)
    for workbook in Workbook.objects.filter(Q(process='Create') | Q(process='Delete')) :
        try:
            tpe.submit(thread_create(workbook))
        except Exception as e:
            print(e)
            errMsg.append(e)
    tpe.shutdown()
    if errMsg:
        raise ValueError(errMsg)
# スレッド
def thread_create(workbook):
    path = workbook.path.replace('\\','/')
    if workbook.process == 'Create':
        print(workbook.book_name)
        file_path=workbook.save_path.replace('\\','/')

        sb.update_or_create(
            workbook.genrue_id,
            workbook.book_id,
            workbook.book_name.strip(),
            file_path,
            workbook.volume,
        )

        if utils.isFile(path):
            utils.fileMove(path, workbook.save_path)        
        else:
            book_util.create_pdf(path, workbook.save_path)
            utils.folder_delete(path)

    elif workbook.process == 'Delete':
        if utils.isFile(path):
            utils.fileDelete(path)
        else:
            utils.folder_delete(path)

    workbook.delete()
# 保存
def update(form, genrue_id, story_by,art_by, title, sub_title, volume):
    workbook = form.save(commit=False)

    extention = utils.getExtention(workbook.path)
    if not extention:
        extention = '.pdf'
    
    genrue       = sg.getObject(genrue_id)
    book_name    = book_util.get_book_name(genrue.genrue_name, story_by, art_by, title, sub_title, volume)
    save_path    = book_util.get_save_path(genrue.genrue_id)
    author_story = sa.commit(story_by)
    author_art   = sa.commit(art_by)

    workbook.process     = "Create"
    workbook.genrue_id   = genrue.genrue_id
    workbook.genrue_name = f"({genrue.genrue_name})"
    workbook.story_by    = author_story.author_name
    workbook.art_by      = author_art.author_name.strip()
    workbook.title       = title.strip()
    workbook.sub_title   = sub_title.strip()
    workbook.volume      = volume
    workbook.book_name   = book_name.strip()
    workbook.save_path   = f"{save_path}{book_name}{extention}"
    workbook.exist_flg   = utils.existFile(save_path + book_name + extention)
    workbook.story_by_id = author_story.id
    workbook.art_by_id   = author_story.id
    
    # シリーズ登録
    series_name = ''
    if genrue.genrue_id < 3:
        series_name = title.strip()
    else:
        series_name = author_story.author_name
    series = ss.series_commit(series_name)

    # 書籍情報登録
    info   = si.info_commit(
        genrue.genrue_id, 
        series.series_name, 
        author_story.id, 
        author_art.id, 
        title, 
        sub_title)
    workbook.book_id = info.id

    workbook.save()

# 全削除
def clear():
    Workbook.objects.all().delete()

def unzip():
    utils.runBat(appconst.UNZIP_BAT)
    # for file in utils.getFiles(appconst.FOLDER_TORRENT, appconst.EXTENTION_ZIP):
    #     utils.unzip(file, appconst.FOLDER_TORRENT)
    #     utils.fileDelete(file)

def convertAvif():
    for folder in utils.getFolders(appconst.FOLDER_TORRENT, appconst.EXTENTION_AVIF):
        utils.convertAvif(folder)