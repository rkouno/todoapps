import re, datetime
from urllib import request

from apps.commons.const import appconst
from apps.commons.util import utils

from .models import Torrent,status


def webscraping():
    dt1 = datetime.datetime.now()
    dt2 = dt1 + datetime.timedelta(days=-30)
    # 削除
    Torrent.objects.filter(regist_date__lt = dt2).delete()

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