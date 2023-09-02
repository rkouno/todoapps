#utils
import urllib.parse
from django.shortcuts import get_object_or_404

#commons
from apps.commons.const import appconst
from apps.commons.util import utils

#db
from django.db.models import Min
from django.db.models import Max
from django.db.models.functions import Coalesce
from apps.anime.models import Anime
from apps.anime.models import Video
from apps.anime.models import Adult

"""
一覧画面
"""
# 一覧
def retriveVideo(tag, sort_code):
    # ソート順
    if sort_code == 1:
        order_colum='group'
        title_group='group'
    elif sort_code == 2:
        order_colum='title'
        title_group='title'
    else:
        order_colum=('-dtRegist')
        title_group='group'

    if appconst.VIDEO in tag:
        videos = Video.objects.filter(process__isnull=True).\
            values('group_id').\
                annotate(last_episode = Min('episode'), 
                        last_id       = Min('id'), 
                        dtRegist      = Max('dtRegist'), 
                        group_title   = Coalesce(Max('group_id__title'), Max('title')),
                        year          = Max('group_id__period_id__year'),
                        season        = Max('group_id__period_id__season'),
                        period        = Max('group_id__period_id__period'),
                        ).\
                    values('last_id', 'group_title', 'last_episode', 'dtRegist', 'year', 'season').\
                        order_by('-year', '-period', order_colum)
    elif appconst.HENTAI in tag:
        videos = Adult.objects.filter(process__isnull=True).\
            values('group').\
                annotate(last_episode = Min('episode'), 
                        last_id       = Min('id'), 
                        dtRegist      = Max('dtRegist'), 
                        group_title   = Max(title_group)).\
                    values('last_id', 'group_title', 'last_episode').\
                        order_by(order_colum)
    return videos

# 移動
def moveVideo():
    folder_path = appconst.FOLDER_TORRENT
    videoFiles = utils.getFiles(folder_path, appconst.EXTENTION_VIDEO)
    for file in videoFiles:
        if utils.isFile(file):
            utils.fileMove(file, appconst.FOLDER_UNWATCH_VIDEO)

# ビデオ登録
def registVideo(tag, unwatched_path, watched_path):
    try:
        # 処理
        if appconst.VIDEO in tag:
            for video in Video.objects.filter(process__exact='delete'):
                # ファイル削除
                utils.fileDelete(video.path)
                video.delete()
            for video in Video.objects.filter(process__exact='move'):
                # ファイル移動
                utils.fileMove(video.path, watched_path)
                video.delete()
            # 削除
            Video.objects.update(process='delete')
        elif appconst.HENTAI in tag:
            for adult in Adult.objects.filter(process__exact='delete'):
                # ファイル削除
                utils.fileDelete(adult.path)
                adult.delete()
            for adult in Adult.objects.filter(process__exact='move'):
                # ファイル移動
                utils.fileMove(adult.path, watched_path)
                adult.delete()
            # 削除
            Adult.objects.update(process='delete')

        # ビデオの登録
        videoFiles = utils.getFiles(unwatched_path, appconst.EXTENTION_VIDEO)
        for file in videoFiles:
            movies = ''
            if appconst.VIDEO in tag:
                movies = Video.objects.filter(path__iexact=file).first()
            elif appconst.HENTAI in tag:
                movies = Adult.objects.filter(path=file).first()
            
            if movies:
                # 既存
                movies.process = None
                movies.save()
            else:
                # 新規
                title = utils.getFileName(file)
                url = file.replace(appconst.FOLDER_MEDIA, appconst.VIDEO_URL)
                url = url.replace(title,urllib.parse.quote(title))
                episode = utils.getRegex(file, '- \d\d').replace('-', '').strip()
                if episode == '':
                    episode = 0
                group = Anime.objects.filter(keyword__icontains = title.split(' - ')[0]).first()
                if group:
                    group = group
                else:
                    group = Anime.objects.get(pk=1)

                # 登録
                if appconst.VIDEO in tag:
                    Video.objects.create(title = title, path = file, episode = episode, url = url, group = group)
                elif tag in appconst.HENTAI:
                    Adult.objects.create(title = title, path = file, episode = episode, url = url, group = title)
    except Exception as e:
        print(e)

# 処理フラグ更新
def updateProcess(tag, id, process):
    if appconst.VIDEO in tag:
        video = getObjectVideo(id)
    elif appconst.HENTAI in tag:
        video = getObjectAdult(id)
    video.process = process
    video.save()

"""
視聴画面
"""
# 視聴
def watch(process, id):
    if process in appconst.VIDEO:
        return getObjectVideo(id)
    elif process in appconst.HENTAI:
        adult = getObjectAdult(id)
        return adult
# 次を視聴
def nextWatch(tag, id):
    if appconst.VIDEO in tag:
        video = getObjectVideo(id)
        next_video = Video.objects.filter(id__gt=id, group=video.group).first()
    elif tag in appconst.HENTAI:
        adult = getObjectAdult(id)
        next_video = Adult.objects.filter(id__gt=id, group=adult.group).first()
    if next_video:
        return next_video
    else:
        return None

"""
共通
"""
# 単一データ取得
def getObjectAnime(pk):
    return get_object_or_404(Anime, pk=pk)
# 単一データ取得
def getObjectVideo(pk):
    return get_object_or_404(Video, pk=pk)
# 単一データ取得
def getObjectAdult(pk):
    return get_object_or_404(Adult, pk=pk)
