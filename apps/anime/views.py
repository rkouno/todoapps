import datetime
from tkinter import Grid

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.anime import serviceAnime, serviceVideo
from apps.anime.forms import AnimeForm
from apps.anime.models import Anime, Video
from apps.commons.const import appconst

# Create your views here.
"""
アニメ
"""
# 一覧
def anime_list(request):
    try:
        # アニメリストを取得
        if request.method == 'GET':
            if len(request.GET) == 0:
                animes = serviceAnime.retriveAnime()
            elif 'download' in request.GET:
                serviceAnime.download()
                animes = serviceAnime.retriveAnime()
            else:
                animes = serviceAnime.retriveAnimeAll()

        return render(request, 'anime/anime_index.html', {'animes' : animes})
    except Exception as e:
        print(e)
    return render(request, 'anime/anime_index.html', {})
# 新規作成
def anime_new(request):
    if request.method == "POST":
        form = AnimeForm(request.POST)
        if form.is_valid():
            serviceAnime.commit(
                form,
                title = request.POST['title'], 
                keyword = request.POST['keyword'],
                dtStart = request.POST['dtStart'],
                dtEnd = request.POST['dtEnd']
            )
  
    form = AnimeForm()
    return render(request, 'anime/anime_edit.html', {'form': form})
# 編集
def anime_edit(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    if "delete" in request.POST:
        anime.delete()
    elif "save" in request.POST:
        form = AnimeForm(request.POST, instance=anime)
        if form.is_valid():
            serviceAnime.commit(
                form,
                title = request.POST['title'], 
                keyword = request.POST['keyword'],
                dtStart = request.POST['dtStart'],
                dtEnd = request.POST['dtEnd']
            )
    else:
        form = AnimeForm(instance=anime)
        return render(request, 'anime/anime_edit.html', {'form': form}) 

    # アニメリストを取得
    animes = serviceAnime.retriveAnimeAll()
    return render(request, 'anime/anime_index.html', {'animes' : animes})

"""
ビデオ
"""
# ダウンロード済みアニメを登録・整理
def video_list(request):
    serviceVideo.registVideo('video', appconst.FOLDER_ROOT_UNWATCH, appconst.FOLDER_VIDEO_WATCHED)
    return redirect('video_index')
# エロアニメを登録
def hentai_list(request):
    serviceVideo.registVideo('adult', appconst.FOLDER_VIDEO_UNWATCHED_HENTAI, appconst.FOLDER_VIDEO_WATCHED_HENTAI)
    return redirect('adult_index')
# 一覧
def video_index(request):
    videos = serviceVideo.retriveVideo('video')
    return render(request, 'video/video_index.html', { 'videos' : videos })
# 一覧
def adult_index(request):
    videos = serviceVideo.retriveVideo('adult')
    return render(request, 'video/video_index.html', { 'videos' : videos })
# 視聴
def video_watch(request, id, tag):
    if "delete" in request.GET:
        serviceVideo.process(tag, id, 'delete')
    elif "next" in request.GET :
        serviceVideo.process(tag, id, 'move')
        video = serviceVideo.next(tag, id)
        if video:
            return redirect('video_watch', id = video.id, tag = 'video')
    elif "watched" in request.GET:
        serviceVideo.process(tag, id, 'move')
    else:
        video  = serviceVideo.watchVideo(tag, id)
        return render(request, 'video/video_watch.html', {'video' : video})

    # 一覧へ戻る
    return redirect(f'{tag}_index')
# ダウンロード
def video_download(request, id):
    video = get_object_or_404(Video, pk=id)
    filename, filepath = video.title, video.path
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
# 削除（論理）
def video_delete(request, id):
    serviceVideo.process(id, 'delete')
     # 一覧へ戻る
    return redirect('video_index')
