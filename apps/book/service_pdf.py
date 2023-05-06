from re import sub
import logging
from django.utils import timezone

from django.db.models import Q
from django.db import transaction
from django.db.models import Min

from apps.book.models import Workbook, Info, Genrue, Status, Book, Author
from apps.commons.const import appconst
from apps.commons.util import utils
from apps.commons.bookutil import book_util

from concurrent.futures import ThreadPoolExecutor

# 初期表示
def retriveWorkbooks():
    return Workbook.objects.all().order_by('-process','book_name', 'name')
def searchWorkbooks(search):
    return Workbook.objects.filter(Q(title__icontains = search) | Q(sub_title__icontains = search)).order_by('-process','book_name', 'name')
# 置換
def replace(txtSearch, txtReplace_b, txtReplace_a, isRegex):
    if isRegex:
        for wb in Workbook.objects.filter(name__icontains = txtSearch):
            wb.name = utils.replace(wb.name, txtReplace_b, txtReplace_a)
            wb.save()
    else:
        for wb in Workbook.objects.filter(name__icontains = txtSearch, name__contains = txtReplace_b):
            wb.name = wb.name.replace(txtReplace_b, txtReplace_a)
            wb.save()
# 一覧取得
def getList():
    # 空フォルダの削除
    utils.folderEmptyDelete(appconst.FOLDER_TORRENT)
    file_folder = []
    # 書籍ファイルの取得
    for book in utils.getFiles(appconst.FOLDER_TORRENT, appconst.EXTENTION_BOOK):
        file_folder.append(book)
    # 書籍フォルダの取得
    for folder in utils.getFolders(appconst.FOLDER_TORRENT, appconst.EXTENTION_IMAGE):
        file_folder.append(folder)
    
    Workbook.objects.all().delete()

    for item in file_folder:
        name = utils.getFileName(item)
        # 登録
        Workbook.objects.create(
            process = 'None',
            path = item,
            name = name,
            genrue_id = 0,
            genrue_name = '',
            story_by_id = 0,
            story_by = '',
            art_by_id = 0,
            art_by = '',
            book_id = 0,
            title = '',
            sub_title = '',
            volume = 0,
            book_name = '',
            save_path = '',
            exist_flg = False,
        )
# 名称設定
def setName():
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

def process(id, process):
    wb = Workbook.objects.get(pk=id)
    wb.process = process
    wb.save()
    
# 編集画面
def retriveWorkbook(pk):
    return Workbook.objects.get(pk=pk)

def delete(id, path):
    if utils.isFile(path):
        utils.fileDelete(path)
    else:
        utils.folder_delete(path)
    Workbook.objects.filter(id=id).delete()

# 保存
def commit(form, genrue_id,story_by,art_by ,title ,sub_title ,volume):
    workbook = form.save(commit=False)

    extention = utils.getExtention(workbook.path)
    if not extention:
        extention = '.pdf'
    
    genrue_model = Genrue.objects.get(pk=genrue_id)
    book_name = book_util.get_book_name(genrue_model.genrue_name, story_by, art_by, title, sub_title, volume)
    status_model=Status.objects.get(pk=1)
    save_path = book_util.get_save_path(genrue_model.genrue_id)

    author_story = author_commit(genrue_id, story_by)
    author_art = author_commit(genrue_id, art_by)

    workbook.process = "Create"
    workbook.genrue_id = genrue_model.genrue_id
    workbook.genrue_name = f"({genrue_model.genrue_name})"
    workbook.story_by = author_story.author_name
    workbook.art_by = author_art.author_name.strip()
    workbook.title = title.strip()
    workbook.sub_title = sub_title.strip()
    workbook.volume = volume
    workbook.book_name = book_name.strip()
    workbook.save_path = save_path + book_name + extention
    workbook.exist_flg = utils.existFile(save_path + book_name + extention)
    workbook.story_by_id = Author.objects.filter(author_name=story_by.strip(), genrue_id=genrue_id).first().author_id
    workbook.art_by_id = Author.objects.filter(author_name=art_by.strip(), genrue_id=genrue_id).first().author_id

    if Info.objects.filter(
        genrue_id = genrue_id,
        story_by_id = author_story.author_id,
        art_by_id = author_art.author_id,
        title = title.strip(),
        sub_title = sub_title.strip(),
    ).count() == 0:
        Info.objects.get_or_create(
            genrue_id = genrue_model.genrue_id,
            story_by_id = author_story.author_id,
            story_by = author_story.author_name.strip(),
            art_by_id = author_art.author_id,
            art_by = author_art.author_name.strip(),
            title = title.strip(),
            sub_title = sub_title.strip(),
            save_path = save_path.strip(),
            status_id = status_model.status_id,
            confirm_date = timezone.now(),
        )
    
    workbook.book_id = Info.objects.filter(
        genrue_id = genrue_id
        , story_by_id = author_story.author_id
        , art_by_id = author_art.author_id
        , title = title.strip()
        , sub_title = sub_title.strip(),
    ).first().book_id

    workbook.save()

@transaction.atomic
def author_commit(genrue_id, author_name):
    authors, created = Author.objects.get_or_create(
        author_name = author_name.strip(),
        genrue_id = genrue_id
    )
    if created:
        authors = Author.objects.filter(genrue_id=genrue_id, author_name=author_name).first()
    return authors

# 作成
def create():
    tpe = ThreadPoolExecutor(max_workers=10)
    for workbook in Workbook.objects.filter(Q(process='Create') | Q(process='Delete')) :
        try:
            tpe.submit(thread_create(workbook))
        except Exception as e:
            print(e)
            logging.info(e)
    tpe.shutdown()

def thread_create(workbook):
    path = workbook.path.replace('\\','/')
    if workbook.process == 'Create':
        print(workbook.book_name)
        file_path=workbook.save_path.replace('\\','/')
        book = Book.objects.filter(file_path=file_path).first()
        if not book:
            bi = Info.objects.get(book_id=workbook.book_id)
            Book.objects.update_or_create(
                genrue_id = workbook.genrue_id,
                genrue_name = workbook.genrue_name.strip(),
                book_id = bi,
                story_by = workbook.story_by,
                story_by_id = workbook.story_by_id,
                art_by_id = workbook.art_by_id,
                art_by = workbook.art_by,
                title = workbook.title,
                sub_title = workbook.sub_title,
                book_name = workbook.book_name.strip(),
                file_path = file_path,
                volume = workbook.volume,
                read_flg = False,
                regist_date = timezone.now(),
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

def next(id):
    # next = Workbook.objects.filter(~Q(process='Create'),~Q(process='Delete'),id__gt=id).aggregate(Min('id'))
    # return next['id__min']
    name = Workbook.objects.get(pk=id).name
    next = Workbook.objects.filter(~Q(process='Create'),~Q(process='Delete'),name__gt=name).order_by('name','volume').first().id
    return next
