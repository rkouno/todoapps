from django.shortcuts import render
from django.utils import timezone
import os
import ctypes

from apps.commons.services.service_torrent import home as service

# Create your views here.
def home_list(request):
    # 過去1週間
    dt = timezone.now() + timezone.timedelta(days=-7)
    # 書籍ダウンロード
    bookTorrents = service.recentBookDownloads(dt)
    # アニメダウンロード
    animeTorrent = service.recentAnimeDownloads(dt)

    return render(request, 'home/home_index.html',{'bookTorrents':bookTorrents,'animeTorrents':animeTorrent})

# シャットダウン 
def shutdown(request):
    #Windowsの終了
    os.system('shutdown -s -f')

# スリープ
def sleep(request):
    #Windowsの休止
    ctypes.windll.PowrProf.SetSuspendState(1, 1, 0)