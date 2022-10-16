import datetime
import re
from tokenize import group
from urllib import request

from django.utils import timezone

from apps.anime.models import Anime, Torrent
from apps.commons.const import appconst
from apps.commons.util import utils

"""
Anime
"""
# 一覧取得（今期のみ）
def retriveAnime():
    return Anime.objects.filter(dtEnd__gte = timezone.now() + datetime.timedelta(days=-14)).order_by('dtUpdate', 'title')
# 一覧取得（全件）
def retriveAnimeAll():
    return Anime.objects.order_by('-dtUpdate', 'title')
# ダウンロード
def download():
    try:
        # Torrentのダウンロード
        for anime in retriveAnime().exclude(keyword=''):
            url = appconst.ANIME_URL % utils.encode(anime.keyword)
            html = utils.WebScraping(url)
            for item in re.split('<item>', str(html)):
                title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
                link = re.search('.*https://nyaa.si/download/.*', item)
                if not link is None:
                    link = link.group().replace('<link/>', '')
                    # torrentファイル名
                    file_name = title + '.torrent'
                    if Torrent.objects.filter(torrent_link = link).count() == 0:
                        # ダウンロード
                        request.urlretrieve(link, appconst.FOLDER_DOWNLOAD + file_name)
                        # ダウンロード済み
                        Torrent.objects.create(
                            title = title,
                            torrent_link = link,
                        )
                        # アニメを更新
                        anime.dtUpdate = timezone.now()
                        anime.save()
    except Exception as e:
        print(e)

# 登録
def commit(form, title, keyword, dtStart, dtEnd):
    anime = form.save(commit=False)
    anime.title = title
    anime.keyword = keyword
    anime.dtStart = dtStart
    anime.dtEnd = dtEnd
    anime.save()
    
    return anime