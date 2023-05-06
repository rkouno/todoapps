from .models import Book, Info, Image, Author, Genrue
from django.db.models import Q
from apps.commons.util import utils
from apps.commons.bookutil import book_util
from apps.commons.const import appconst
from django.db.models import Max

def retriveInfo(genrue_id):
    # bookinfo = Info.objects.filter(genrue_id=genrue_id).\
    #     select_related('book_id').order_by('regist_date').\
    #         values('title').\
    #             annotate(book_id=Max('book_id')).\
    #                 values('book_id', "title")
    bookinfo = Book.objects.filter(genrue_id=genrue_id)\
        .values('title')\
            .annotate(book_id=Max('book_id'),regist_date=Max('regist_date'))\
                .values('book_id','title')\
                    .order_by('-regist_date')
    return bookinfo
def retriveFix():
    sql = 'SELECT '\
        + '      BB.SLUG '\
        + '    , BB.GENRUE_ID '\
        + '    , BB.GENRUE_NAME '\
        + '    , BB.BOOK_ID_ID '\
        + '    , BB.BOOK_NAME '\
        + '    , BB.FILE_PATH '\
        + '    , BB.VOLUME '\
        + '    , BB.READ_FLG '\
        + '    , BB.REGIST_DATE '\
        + 'FROM '\
        + '    BOOK_BOOK BB '\
        + '    LEFT JOIN BOOK_INFO BI '\
        + '        ON BB.GENRUE_ID = BI.GENRUE_ID '\
        + '        AND BB.BOOK_ID_ID = BI.BOOK_ID '\
        + 'WHERE '\
        + '    BI.BOOK_ID IS NULL '\
        + 'ORDER BY '\
        + '    BOOK_NAME '

    books = Book.objects.raw(sql)
    return books

def check():
    noneBooks = []
    books=Book.objects.all()
    for b in books:
        if not utils.existFile(b.file_path):
            noneBooks.append(b)
            print(b.file_path)
    return noneBooks

def check2():
    noneBooks = []
    for file in utils.getFiles(appconst.FOLDER_ROOT_BOOK, appconst.EXTENTION_BOOK):
        b = Book.objects.filter(file_path=file.replace('\\','/')).first()
        if not b:
            noneBooks.append(file)
            print(file)
    return noneBooks

def retriveBooks(book_id):
    sql = "SELECT "\
        + "      * "\
        + "FROM "\
        + "    BOOK_BOOK BB "\
        + "    INNER JOIN ( "\
        + "        SELECT DISTINCT "\
        + "              BI.GENRUE_ID "\
        + "              , BI.TITLE  "\
        + "        FROM "\
        + "            BOOK_INFO BI "\
        + "            LEFT JOIN BOOK_BOOK BB "\
        + "                ON BI.BOOK_ID = BB.BOOK_ID_ID "\
        + "        WHERE "\
        + f"            BI.BOOK_ID = {book_id}" \
        + "    ) S "\
        + "        ON S.TITLE = BB.TITLE "\
        + "        AND S.GENRUE_ID = BB.GENRUE_ID "\
        + "ORDER BY "\
        + "    BB.READ_FLG DESC "\
        + "    , CAST(BB.VOLUME AS INT)"\

    books = Book.objects.raw(sql)
    return books

def retriveAdultBooks(author_id):
    sql = "SELECT "\
        + "      FILE_PATH "\
        + "    , BOOK_NAME "\
        + "    , READ_FLG "\
        + "FROM "\
        + "    BOOK_BOOK BB "\
        + "    INNER JOIN BOOK_INFO BI "\
        + "        ON BB.GENRUE_ID = BI.GENRUE_ID "\
        + "        AND BB.BOOK_ID_ID = BI.BOOK_ID "\
        + "WHERE "\
        + f"    BI.STORY_BY_ID = { author_id } "\
        + f"    OR BI.ART_BY_ID = { author_id } "

    books = Book.objects.raw(sql)
    return books

def retriveAuthors():
    sql ="SELECT DISTINCT "\
        + "      A.* "\
        + "      , CASE WHEN MIN(BB.READ_FLG) = 1 THEN 'True' ELSE 'False' END AS read_flg "\
        + "FROM "\
        + "    BOOK_AUTHOR A "\
        + "    INNER JOIN BOOK_BOOK BB "\
        + "        ON A.AUTHOR_ID = BB.STORY_BY_ID "\
        + "WHERE "\
        + "    A.GENRUE_ID IN (3, 4) "\
        + "    GROUP BY "\
        + "    A.AUTHOR_ID "\
        + "    , A.AUTHOR_NAME "\
        + "    , A.GENRUE_ID "\
        + "ORDER BY "\
        + "    BB.READ_FLG ASC " \
        + "    , BB.REGIST_DATE DESC "

    authors = Author.objects.raw(sql)
    return authors
import logging
def download(id):
    b = Book.objects.filter(slug=id).first()
    b.read_flg = True
    b.save()
    return b.file_path

def retriveBookInfo(genrue_id, title, sub_title):
    sql = f"SELECT book_id, story_by_id, story_by, art_by_id, art_by, title, sub_title, save_path, confirm_date, genrue_id, status_id FROM BOOK_INFO WHERE (TITLE LIKE '%' || '{title}' || '%' OR '{title}' LIKE '%' || TITLE || '%') AND (SUB_TITLE LIKE '%' || '{sub_title}' || '%' OR '{sub_title}' LIKE '%' || SUB_TITLE || '%' OR '' = '') AND ({genrue_id} = 0 OR GENRUE_ID = {genrue_id})"
    bookinfo = Info.objects.raw(sql)
    return bookinfo

def retriveImage(path):
    
    Image.objects.all().delete()

    for list in utils.getFiles(f'{path}/', appconst.EXTENTION_IMAGE):
        list = list.replace('\\','/')
        url = list.replace(appconst.FOLDER_TORRENT, appconst.TORRENT_URL)
        Image.objects.create(img_link = url)

    return Image.objects.all()

def delete(path):
    if utils.isFile(path) or utils.existFile(path):
        utils.fileDelete(path)
    elif utils.isDir(path):
        utils.folder_delete(path)

    Book.objects.get(pk=path).delete()

def commit(form,pk):
    b = Book.objects.filter(slug=pk).first()

    before_file_path = form.instance.file_path

    extention = utils.getExtention(form.instance.file_path)
    genrue_id = book_util.get_genrue_id(form.instance.genrue_name) 
    genrue_name = get_genrue_name(genrue_id)

    story_by_id = get_author_id(form.instance.genrue_id, form.instance.story_by)
    story_by = form.instance.story_by

    art_by_id = get_author_id(form.instance.genrue_id, form.instance.art_by or '')
    art_by = form.instance.art_by or ''

    title = form.instance.title
    sub_title = form.instance.sub_title or ''
    volume = form.instance.volume or ''
    
    book_name = book_util.get_book_name(genrue_name, story_by, art_by, title, sub_title, volume)
    file_path = book_util.get_save_path(genrue_id)

    b.book_id = get_book_id(
        genrue_id,
        story_by_id,
        story_by,
        art_by_id,
        art_by,
        title,
        sub_title
    )

    b.genrue_id = genrue_id
    b.genrue_name = genrue_name
    b.story_by_id = story_by_id
    b.story_by = story_by
    b.art_by_id = art_by_id
    b.art_by = art_by
    b.title = title
    b.sub_title = sub_title
    b.volume = volume

    b.book_name = book_name
    after_file_path =file_path + book_name + extention
    b.file_path = after_file_path
    b.slug = None

    if not utils.existFile(after_file_path):
        b.save()
    else:
        Book.objects.filter(slug=pk).first().delete()

    if not before_file_path == after_file_path:
        utils.fileMove(before_file_path, after_file_path)


def get_author_id(genrue_id, author_name):
    a, created = Author.objects.get_or_create(
        author_name = author_name,
        genrue_id = genrue_id
    )
    if created:
        a = Author.objects.filter(author_name=author_name, genrue_id=genrue_id).first()

    return a.author_id

def get_genrue_name(genrue_id):
    return Genrue.objects.get(pk=genrue_id).genrue_name

def get_book_id(genrue_id, story_by_id ,story_by, art_by_id ,art_by, title, sub_title):
    save_path = ''
    if genrue_id == appconst.COMIC:
        save_path = appconst.FOLDER_BOOK_COMIC
    elif genrue_id == appconst.NOVEL:
        save_path = appconst.FOLDER_BOOK_NOVEL
    elif genrue_id == appconst.ADULT:
        save_path = appconst.FOLDER_BOOK_ADULT
    elif genrue_id == appconst.ADULT_NOVEL:
        save_path == appconst.FOLDER_BOOK_ADULT_NOVEL

    bi = Info.objects.filter(genrue_id=genrue_id, story_by_id=story_by_id, art_by_id=art_by_id, title=title, sub_title=sub_title).first()
    if not bi:
        bi, created = Info.objects.get_or_create(
            genrue_id = genrue_id,
            story_by_id = story_by_id,
            story_by = story_by,
            art_by = art_by,
            art_by_id = art_by_id,
            title = title, 
            sub_title = sub_title,
            status_id = 0,
            save_path = save_path
        )
        bi = Info.objects.filter(genrue_id=genrue_id, title=title, sub_title=sub_title).first()

    return bi