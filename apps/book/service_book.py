from .models import book, info, Image, author, genrue
from django.db.models import Q
from apps.commons.util import utils
from apps.commons.bookutil import book_util
from apps.commons.const import appconst
from django.db.models import Max

def retriveInfo(genrue_id):
    bookinfo = info.objects.filter(genrue_id=genrue_id).\
            values('title').\
                annotate(book_id=Max('book_id')).\
                    values('book_id', "title")
    return bookinfo
def retriveFix():
    sql = 'SELECT '\
        + '      BB.ID '\
        + '    , BB.GENRUE_ID '\
        + '    , BB.GENRUE_NAME '\
        + '    , BB.BOOK_ID '\
        + '    , BB.BOOK_NAME '\
        + '    , BB.FILE_PATH '\
        + '    , BB.VOLUME '\
        + '    , BB.READ_FLG '\
        + '    , BB.REGIST_DATE '\
        + 'FROM '\
        + '    BOOK_BOOK BB '\
        + '    LEFT JOIN BOOK_INFO BI '\
        + '        ON BB.GENRUE_ID = BI.GENRUE_ID '\
        + '        AND BB.BOOK_ID = BI.BOOK_ID '\
        + 'WHERE '\
        + '    BI.BOOK_ID IS NULL '\
        + 'ORDER BY '\
        + '    BOOK_NAME '

    books = book.objects.raw(sql)
    return books

def retriveBooks(book_id):
    books = book.objects.filter(book_id=book_id).order_by('read_flg')
    return books

def retriveAdultBooks(author_id):
    sql = "SELECT "\
        + "      ID "\
        + "    , BOOK_NAME "\
        + "    , READ_FLG "\
        + "FROM "\
        + "    BOOK_BOOK BB "\
        + "    INNER JOIN BOOK_INFO BI "\
        + "        ON BB.GENRUE_ID = BI.GENRUE_ID "\
        + "        AND BB.BOOK_ID = BI.BOOK_ID "\
        + "WHERE "\
        + f"    BI.STORY_BY_ID = { author_id } "\
        + f"    OR BI.ART_BY_ID = { author_id } "

    books = book.objects.raw(sql)
    return books

def retriveAuthors():
    authors = author.objects.filter(Q(genrue_id=3) | Q(genrue_id=4), author_name__gt="")
    return authors

def download(id):
    b = book.objects.get(pk=id)
    b.read_flg = True
    b.save()
    return b.file_path , b.book_name

def retriveBookInfo(genrue_id, title, sub_title):
    sql = f"SELECT book_id, story_by_id, story_by, art_by_id, art_by, title, sub_title, save_path, confirm_date, genrue_id, status_id FROM BOOK_INFO WHERE (TITLE LIKE '%' || '{title}' || '%' OR '{title}' LIKE '%' || TITLE || '%') AND (SUB_TITLE LIKE '%' || '{sub_title}' || '%' OR '{sub_title}' LIKE '%' || SUB_TITLE || '%' OR '' = '') AND ({genrue_id} = 0 OR GENRUE_ID = {genrue_id})"
    bookinfo = info.objects.raw(sql)
    return bookinfo

def retriveImage(path):
    
    Image.objects.all().delete()

    for list in utils.getFiles(f'{path}/', appconst.EXTENTION_IMAGE):
        list = list.replace('\\','/')
        url = list.replace(appconst.FOLDER_TORRENT, appconst.TORRENT_URL)
        Image.objects.create(img_link = url)

    return Image.objects.all()

def delete(id, path):
    if utils.isFolder(path):
        utils.folder_delete(path)
    else:
        utils.fileDelete(path)

    book.objects.get(pk=id).delete()

def commit(form):
    b = book.objects.get(pk=form.instance.id)

    before_file_path = form.instance.file_path

    extention = utils.getExtention(form.instance.file_path)
    genrue_id = form.instance.genrue_id
    genrue_name = get_genrue_name(form.instance.genrue_id)

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

    b.save()

    if not before_file_path == after_file_path:
        utils.fileMove(before_file_path, after_file_path)


def get_author_id(genrue_id, author_name):
    a, created = author.objects.get_or_create(
        author_name = author_name,
        genrue_id = genrue_id
    )
    if created:
        a = author.objects.filter(author_name=author_name, genrue_id=genrue_id).first()

    return a.author_id

def get_genrue_name(genrue_id):
    return genrue.objects.get(pk=genrue_id).genrue_name

def get_book_id(genrue_id, story_by_id ,story_by, art_by_id ,art_by, title, sub_title):
    if genrue_id == appconst.COMIC:
        save_path = appconst.FOLDER_BOOK_COMIC
    elif genrue_id == appconst.NOVEL:
        save_path = appconst.FOLDER_BOOK_NOVEL
    elif genrue == appconst.ADULT:
        save_path = appconst.FOLDER_BOOK_ADULT
    elif genrue_id == appconst.ADULT_NOVEL:
        save_path == appconst.FOLDER_BOOK_ADULT_NOVEL

    bi = info.objects.filter(genrue_id=genrue_id, story_by_id=story_by_id, art_by_id=art_by_id, title=title, sub_title=sub_title).first()
    if not bi:
        bi, created = info.objects.get_or_create(
            genrue_id = genrue_id,
            story_by_id = story_by_id,
            story_by = story_by,
            art_by = art_by,
            art_by_id = art_by_id,
            title = title, 
            sub_title = sub_title,
            status_id = False,
            save_path = save_path
        )
        bi = info.objects.filter(genrue_id=genrue_id, title=title, sub_title=sub_title).first()

    return bi.book_id