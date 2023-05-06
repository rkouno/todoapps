#utils
import re
import datetime
from urllib import request
from django.utils import timezone
from django.shortcuts import get_object_or_404

#commons
from apps.commons.const import appconst
from apps.commons.util import utils

#django db
from apps.anime.models import Anime
from apps.anime.models import Period
from apps.anime.models import Torrent
from apps.anime.models import Adult

class download:
    """
    一覧画面
    """
    # ダウンロードアニメ一覧の取得
    def retriveAnime(isEnd):
        if isEnd:
            animes = Anime.objects.all().order_by('-period', '-dtUpdate', 'title')    
        else:
            animes = Anime.objects.filter(isEnd=isEnd, dtStart__lt=timezone.now()).order_by('-period', '-dtUpdate', 'title')
        return animes

    # ダウンロード
    def download():
        try:
            # Torrentのダウンロード
            for anime in download.retriveAnime(False).exclude(keyword=''):
                url = appconst.ANIME_URL % utils.encode(anime.keyword)
                html = utils.WebScraping(url)
                for item in re.split('<item>', str(html)):
                    title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
                    link = re.search('.*https://nyaa.si/download/.*', item)
                    if link:
                        link = link.group().replace('<link/>', '')
                        # torrentファイル名
                        file_name = f'{title}.torrent'
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
                            if "END" in title:
                                anime.isEnd = True
                            anime.save()
        except Exception as e:
            print(e)
    """
    登録画面
    """
    # 登録
    def commit(form, title, keyword, id):
        period = Period.objects.get(pk=id)
        # 1：冬　1 ~ 3
        # 2：春　4 ~ 6
        # 3：夏　7 ~ 9
        # 4：秋　10~ 12
        start_month = 1 if period.period == 1 else 4 if period.period == 2 else 7 if period.period == 3 else 10
        end_month = 3 if period.period == 1 else 6 if period.period == 2 else 9 if period.period == 3 else 12
        anime = form.save(commit=False) 
        anime.title = title
        anime.keyword = keyword
        anime.dtStart = f"{period.year}-{str(start_month).zfill(2)}-01"
        anime.dtEnd = utils.get_last_date(period.year, end_month)
        anime.period = period
        anime.save()
        
        return anime
    # シーズン作成
    def CreatePeriod():
        dt = datetime.datetime.now()
        dt2 = dt + datetime.timedelta(days=-30)

        year = dt2.year
        month = dt2.month
        period = 4 if month >= 10 else 3 if month >= 7 else 2 if month >= 4 else 1
        season = '秋' if month >= 10 else '夏' if month >= 7 else '春' if month >= 4 else '冬'
        
        if not Period.objects.filter(season=season, year=year):
            Period.objects.get_or_create(
                year = year
                , period = period
                , season = season
            )

class master:
    def retriveAdultVideo():
        adults = Adult.objects.all()
        return adults

    def getAdultObject(id):
        return get_object_or_404(Adult, pk=id)

    def commit(id, title, group):
        adult = Adult.objects.get(pk=id)
        adult.title = title
        adult.group = group
        adult.save()