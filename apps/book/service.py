from urllib import request
from .models import Torrent
from apps.commons.const import appconst
from apps.commons.util import utils

import re

def webscraping():
    # 削除
    Torrent.objects.all().delete()

    # Web Scraping
    url = appconst.SUKEBEI_URL
    html = utils.WebScraping(url)
    for item in re.split('<item>', str(html)):
        title = re.search('<title>.*</title>', item).group().replace('<title>', '').replace('</title>', '')
        link = re.search('.*https://sukebei.nyaa.si/download/.*', item)
        if not link is None:
           link = link.group().replace('<link/>', '')

        nyaa_content = re.search('.*https://sukebei.nyaa.si/view/.*', item)
        if not nyaa_content is None:
            nyaa_content = nyaa_content.group()
            hentai_cover_url = ''
            nyaa_content = re.split('<',re.split('>', nyaa_content)[1])[0]
            hentai_html = utils.WebScraping(nyaa_content)
            hentai_cover_url = re.search('.*https://hentai-covers.site/image/.*', str(hentai_html))
            if not hentai_cover_url is None:
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
    return Torrent.objects.filter(img_link__isnull=False)

def download(id):
    torrent = Torrent.objects.get(id=id)
    title = torrent.title + '.torrent'
    request.urlretrieve(torrent.torrent_link, appconst.FOLDER_DOWNLOAD + title)