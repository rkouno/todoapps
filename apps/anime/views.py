# utils
from django.http import FileResponse
from django.shortcuts import redirect
from django.shortcuts import render

# commons
from apps.commons.const import appconst

# form
from apps.anime.forms import AnimeForm

# service
from apps.commons.services import service_video as sv
from apps.commons.services.service_anime import download as sab

# Create your views here.
"""
アニメ
"""
# 一覧
def anime_list(request):
    # アニメリストを取得
    try:
        if request.method == 'GET':
            if 'all' in request.GET:
                # 全件表示
                animes = sab.retriveAnime(True)
            elif 'download' in request.GET:
                # ダウンロード
                sab.download()
                animes = sab.retriveAnime(False)
            else:
                # 初期表示
                animes = sab.retriveAnime(False)
            return render(request, 'anime/anime_index.html', {'animes' : animes})
    except Exception as e:
        print(e)

    return render(request, 'anime/anime_index.html')
# 新規作成
def anime_new(request):
    if request.method == "POST":
        form = AnimeForm(request.POST)
        if form.is_valid():
            sab.commit(
                form,
                title   = request.POST['title'], 
                keyword = request.POST['keyword'],
                id      = request.POST['period']
            )
    else:
        sab.CreatePeriod()
    form = AnimeForm()
    return render(request, 'anime/anime_edit.html', {'form': form})
# 編集
def anime_edit(request, pk):
    anime = sv.getObjectAnime(pk)
    if "delete" in request.POST:
        anime.delete()
    elif "save" in request.POST:
        form = AnimeForm(request.POST, instance=anime)
        if form.is_valid():
            sab.commit(
                form,
                title = request.POST['title'], 
                keyword = request.POST['keyword'],
                id = request.POST['period']
            )
    else:
        initial = dict(isEnd = anime.isEnd)
        form = AnimeForm(instance=anime, initial=initial)
        return render(request, 'anime/anime_edit.html', {'form': form}) 
    return redirect('anime_list')

"""
ビデオ
"""
# 一覧(一般)
def video_index(request, sort_code):
    request.session['sort_code'] = sort_code
    videos = sv.retriveVideo(appconst.VIDEO, sort_code)
    return render(request, 'video/video_index.html', { 'videos' : videos, 'sort_code' : sort_code})
# 一覧(エロアニメ)
def hentai_index(request, sort_code):
    request.session['sort_code'] = sort_code
    videos = sv.retriveVideo(appconst.HENTAI, sort_code)
    return render(request, 'video/video_index.html', { 'videos' : videos, 'sort_code' : sort_code})
# ダウンロード済みアニメを登録・整理
def video_list(request):
    sv.registVideo(appconst.VIDEO, appconst.FOLDER_UNWATCH_VIDEO, appconst.FOLDER_WATCHED_VIDEO)
    return redirect('video_index', appconst.SORT_RECENT)
# エロアニメを登録
def hentai_list(request):
    sv.registVideo(appconst.HENTAI, appconst.FOLDER_UNWATCH_HENTAI, appconst.FOLDER_WATCHED_HENTAI)
    return redirect('hentai_index', appconst.SORT_RECENT)
# 一覧・削除（論理）
def video_delete(request, id, tag):
    sv.updateProcess(tag, id, 'delete')
    return redirect('video_index', request.session['sort_code'])
# 視聴画面・ボタン操作
def video_watch(request, id, tag):
    sort_code=request.session['sort_code']
    if "delete" in request.GET:
        sv.updateProcess(tag, id, 'delete')
        video = sv.nextWatch(tag, id)
        if video:
            return redirect('video_watch', video.id, tag)
    elif "next" in request.GET :
        sv.updateProcess(tag, id, 'move')
        video = sv.nextWatch(tag, id)
        if video:
            return redirect('video_watch', video.id, tag)
    elif "watched" in request.GET:
        sv.updateProcess(tag, id, 'move')
    else:
        video  = sv.watch(tag, id)
        return render(request, 'video/video_watch.html', {appconst.VIDEO : video})
    # 一覧へ戻る
    return redirect(f'{tag}_index', sort_code)
# 一覧/視聴画面・ダウンロード
def video_download(request, id, tag):
    if tag in appconst.VIDEO:
        media = sv.getObjectVideo(id)
    else:
        media = sv.getObjectAdult(id)
    sv.updateProcess(tag, id, 'move')
    filename, filepath = media.title, media.path
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
