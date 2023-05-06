import re, datetime
from urllib import request

from django.db.models import Q, Max

from apps.commons.const import appconst
from apps.commons.util import utils
from .models import Torrent,Status,Author,Info,Book

def webscraping():
    dt1 = datetime.datetime.now()
    dt2 = dt1 + datetime.timedelta(days=-30)
    # 削除
    Torrent.objects.filter(regist_date__lt = dt2, genrue_id=appconst.ADULT).delete()

    # Web Scraping
    url = appconst.SUKEBEI_URL
    html = utils.WebScraping(url)
    for item in re.split('<item>', str(html)):
        title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
        link = re.search('.*https://sukebei.nyaa.si/download/.*', item)
        if link:
            link = link.group().replace('<link/>', '')
            cnt = Torrent.objects.filter(torrent_link=link).count()
            if cnt == 0:
                nyaa_content = re.search('.*https://sukebei.nyaa.si/view/.*', item)
                if nyaa_content:
                    nyaa_content = nyaa_content.group()
                    hentai_cover_url = ''
                    nyaa_content = re.split('<',re.split('>', nyaa_content)[1])[0]
                    hentai_html = utils.WebScraping(nyaa_content)
                    hentai_cover_url = re.search('.*https://hentai-covers.site/image/.*', str(hentai_html))
                    if hentai_cover_url:
                        hentai_cover_url = hentai_cover_url.group().replace('**','').replace('</div>', '')
                        hentai_html = utils.WebScraping(hentai_cover_url)
                        hentai_cover_url = re.search('src="https://hentai-covers.site/images/.*', str(hentai_html))
                        hentai_cover_url = re.split(' ', re.split('src="', hentai_cover_url.group())[1])[0].replace('"','')

                    # 登録
                    Torrent.objects.create(
                        genrue_id = appconst.ADULT,
                        title = title,
                        torrent_link = link,
                        img_link = hentai_cover_url
                    )

def retriveTorrent():
    # 取得
    return Torrent.objects.filter(img_link__isnull=False, downloaded=False).order_by('-regist_date')

def download(id):
    torrent = Torrent.objects.get(id=id)
    title = torrent.title + '.torrent'
    
    torrent.downloaded = True
    torrent.save()
    
    request.urlretrieve(torrent.torrent_link, appconst.FOLDER_DOWNLOAD + title)

def status():
    return status.objects.all()

def retriveNyasBooks():
    books = Info.objects.filter(Q(genrue_id=appconst.COMIC)|Q(genrue_id=appconst.NOVEL), status_id=0)\
        .values('title')\
            .annotate(m_book_id=Max("book_id"), m_confirm_date=Max('confirm_date'))\
                .values("m_confirm_date", "m_book_id", "title").\
                    order_by("confirm_date")
    return books

def retriveSukebeBooks():
    sql = "SELECT "\
        + "      BA.AUTHOR_ID "\
        + "    , BA.AUTHOR_NAME "\
        + "    , BA.GENRUE_ID "\
        + "FROM "\
        + "    BOOK_AUTHOR BA "\
        + "    LEFT JOIN BOOK_INFO BI "\
        + "        ON BI.STORY_BY_ID = BA.AUTHOR_ID "\
        + "WHERE "\
        + "    BA.GENRUE_ID = 3 "\
        + "    AND BA.AUTHOR_NAME <> '' "\
        + "GROUP BY "\
        + "    BA.AUTHOR_ID "\
        + "    , BA.AUTHOR_NAME "\
        + "    , BA.GENRUE_ID "\
        + "ORDER BY "\
        + "    MAX(BI.CONFIRM_DATE) ASC "
    authors = Author.objects.raw(sql)

    return authors

def authorName(pk):
    author_name = Author.objects.get(pk=pk).author_name
    return author_name

def bookTitle(pk):
    title = Info.objects.get(pk=pk).title
    return title

def nyaascraping(word, url, pk):
    url = url % utils.encode(word)
    html = utils.WebScraping(url)
    try:
        for item in re.split('<item>', str(html)):
            title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
            link = re.search('.*https://nyaa.si/download/.*', item)
            if link:
                link = link.group().replace('<link/>', '')
                if Torrent.objects.filter(torrent_link = link).count() == 0:
                    # ダウンロードリスト追加
                    Torrent.objects.create(
                        title = title,
                        torrent_link = link,
                        img_link = None,
                        downloaded = False,
                        genrue_id = appconst.COMIC,
                        book_id = pk
                    )
    except Exception as e:
        print(e)

def updateInfo(pk):
    bi = Info.objects.get(pk=pk).update()

def retriveDownloadBooks(pk):
    torrents = Torrent.objects.filter(book_id = pk, downloaded=False).order_by('-regist_date')
    return torrents
def retriveBooks(pk):
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
        + f"            BI.BOOK_ID = {pk}" \
        + "    ) S "\
        + "        ON S.TITLE = BB.TITLE "\
        + "ORDER BY "\
        + "    BB.GENRUE_ID "\
        + "    , BB.TITLE "\
        + "    , BB.SUB_TITLE "\
        + "    , CAST(BB.VOLUME AS INT) "\

    books = Book.objects.raw(sql)
    return books