# util
from django.shortcuts import get_object_or_404
from concurrent.futures import ThreadPoolExecutor
from django.db.models import Q
from django.db import transaction

# service
from apps.commons.services import service_bookInfo as sb
from apps.commons.services import service_series as ss
from apps.commons.services import service_author as sa

# common
from apps.commons.util import utils
from apps.commons.bookutil import book_util
from apps.commons.const import appconst

# db
from apps.book.models import Workbook
from apps.book.models import Book
from apps.book.models import Info
from apps.book.models import Author
from apps.book.models import Genrue
from apps.book.models import Status
from apps.book.models import Series

"""
Book
"""
# 初期表示
def retriveWorkbooks(text):
    if text:
        search = Q(name__icontains = text)
    else:
        search = Q()
    return Workbook.objects.filter(search).order_by('-process','book_name', 'name')
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

        art_by = book_util.get_author(name)
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
        for wb in Workbook.objects.filter(name__icontains = before):
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
    tpe = ThreadPoolExecutor(max_workers=10)
    for workbook in Workbook.objects.filter(Q(process='Create') | Q(process='Delete')) :
        try:
            tpe.submit(thread_create(workbook))
        except Exception as e:
            print(e)
    tpe.shutdown()
# スレッド
def thread_create(workbook):
    path = workbook.path.replace('\\','/')
    if workbook.process == 'Create':
        print(workbook.book_name)
        file_path=workbook.save_path.replace('\\','/')
        bi = Info.objects.get(book_id=workbook.book_id)
        Book.objects.update_or_create(
            genrue    = Genrue.objects.get(pk=workbook.genrue_id),
            book      = Info.objects.get(pk=workbook.book_id),
            series    = bi.series,
            book_name = workbook.book_name.strip(),
            file_path = file_path,
            volume    = workbook.volume,
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
def commit(form, genrue_id, story_by,art_by, title, sub_title, volume):
    workbook = form.save(commit=False)

    extention = utils.getExtention(workbook.path)
    if not extention:
        extention = '.pdf'
    
    genrue       = Genrue.objects.get(pk=genrue_id)
    book_name    = book_util.get_book_name(genrue.genrue_name, story_by, art_by, title, sub_title, volume)
    save_path    = book_util.get_save_path(genrue.genrue_id)
    author_story = sa.author_commit(genrue_id, story_by)
    author_art   = sa.author_commit(genrue_id, art_by)

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
    workbook.story_by_id = author_story.author_id
    workbook.art_by_id   = author_story.author_id
    
    # シリーズ登録
    series_name = ''
    if genrue.genrue_id < 3:
        series_name = title.strip()
    else:
        series_name = author_story.author_name
    series = ss.series_commit(series_name)

    # 書籍情報登録
    info   = sb.info_commit(
        genrue.genrue_id, 
        series.series_id, 
        author_story.author_id, 
        author_art.author_id, 
        title, 
        sub_title)
    workbook.book_id = info.book_id

    workbook.save()

