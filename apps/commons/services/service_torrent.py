# util
import re
import datetime
from urllib import request
from django.shortcuts import get_object_or_404

# common
from apps.commons.const import appconst
from apps.commons.util import utils

#model
from apps.anime.models import Torrent as at
from apps.book.models import Torrent as bt

# service 

"""
home
"""
class home:
    # 直近ダウンロード（書籍）
    def recentBookDownloads(dt):
        bookTorrents = bt.objects.filter(regist_date__gt=dt, downloaded=1).order_by('-regist_date')
        return bookTorrents
    # 直近ダウンロード（アニメ）
    def recentAnimeDownloads(dt):
        animeTorrent = at.objects.filter(dtRegist__gt=dt).order_by('-dtRegist')
        return animeTorrent

"""
Download
"""
class download:
    # Webscrapping
    def sukebei_webscrapping():
        dt1 = datetime.datetime.now()
        dt2 = dt1 + datetime.timedelta(days=-14)
        # 削除
        bt.objects.filter(regist_date__lt = dt2, adult_flg=True).delete()

        # Web Scraping
        url = appconst.SUKEBEI_URL
        html = utils.WebScraping(url)
        for item in re.split('<item>', str(html)):
            title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
            link = re.search('.*https://sukebei.nyaa.si/download/.*', item)
            if link:
                link = link.group().replace('<link/>', '')
                cnt = bt.objects.filter(torrent_link=link).count()
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
                        bt.objects.create(
                            title        = title,
                            torrent_link = link,
                            img_link     = hentai_cover_url,
                            adult_flg    = True,
                        )

    def nyaa_webscrapping():
        dt1 = datetime.datetime.now()
        dt2 = dt1 + datetime.timedelta(days=-14)
        # 削除
        bt.objects.filter(regist_date__lt = dt2, adult_flg=False, downloaded=False, series__isnull=True).delete()
        # Web Scraping
        url = appconst.BOOK_URL
        html = utils.WebScraping(url)
        try:
            for item in re.split('<item>', str(html)):
                title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
                link = re.search(appconst.BOOK_DL_URL, item)
                if link:
                    link = link.group().replace('<link/>', '')
                        # ダウンロードリスト追加
                    bt.objects.get_or_create(
                        title = title,
                        torrent_link = link,
                        series = None
                    )
        except Exception as e:
            print(e)

# 取得
def retriveTorrentAdult():
    return bt.objects.filter(adult_flg=True, downloaded=False).order_by('-regist_date')
    
# 取得
def retriveTorrentNyaa():
    return bt.objects.filter(adult_flg=False, downloaded=False, series__isnull=True).order_by('-regist_date')

# ダウンロードリストに追加
def scraping(keyword, url, url2, series):
    url = url % utils.encode(keyword)
    html = utils.WebScraping(url)
    try:
        for item in re.split('<item>', str(html)):
            title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
            link = re.search(url2, item)
            if link:
                link = link.group().replace('<link/>', '')
                    # ダウンロードリスト追加
                bt.objects.update_or_create(
                    torrent_link = link,
                    defaults = {
                        'title'  : title,
                        'series' : series,
                    },
                )
    except Exception as e:
        print(e)

# ダウンロードリスト
def downloadList(series_id):
    torrents = bt.objects.filter(series_id = series_id, downloaded=False).order_by('-regist_date', 'title')
    return torrents
"""
共通
"""
# Torrent(Book)
def getObjectBookTorrent(pk):
    return bt.objects.get(pk=pk)
# Torrent(Anime)
def getObjectAnimeTorrent(pk):
    return at.objects.get(pk=pk)
# ダウンロード済み更新（Anime）
def updAnimeTorrent(pk):
    anime = at.objects.get(pk=pk)
    anime.downloaded = True
    anime.save() 
# Torrentファイルのダウンロード
def downloadTorrentFile(link, text):
    title = text + '.torrent'
    request.urlretrieve(link, appconst.FOLDER_DOWNLOAD + title)
# ダウンロード済み更新（Book）
def updBookTorrent(pk):
    anime = bt.objects.get(pk=pk)
    anime.downloaded = True
    anime.save() 