from django.db.models import Min
from apps.commons.const import appconst
from apps.commons.util import utils
from .models import Adult, Anime, Video

import urllib.parse

"""
Video
"""
# ビデオ取得
def registVideo(tag, folder_path, watched_path):
    try:
        # 処理
        if tag in 'video':
            for video in Video.objects.filter(process__exact='delete'):
                # ファイル削除
                utils.fileDelete(video.path)
            for video in Video.objects.filter(process__exact='move'):
                # ファイル移動
                utils.fileMove(video.path, watched_path)
            # 削除
            Video.objects.all().delete()
        elif tag in 'adult':
            for adult in Adult.objects.filter(process__exact='delete'):
                # ファイル削除
                utils.fileDelete(adult.path)
            for adult in Adult.objects.filter(process__exact='move'):
                # ファイル移動
                utils.fileMove(adult.path, watched_path)
            # 削除
            Adult.objects.all().delete()

        # ビデオの登録
        videoFiles = utils.getFiles(folder_path, appconst.EXTENTION_VIDEO)
        for file in videoFiles:
            title = utils.getFileName(file)
            url = file.replace(appconst.FOLDER_MEDIA, appconst.URL)
            url = url.replace(title,urllib.parse.quote(title))
            episode = utils.getRegex(file, '- \d\d').replace('-', '').strip()
            if episode == '':
                episode = 0
            group = Anime.objects.filter(keyword__icontains = title.split(' - ')[0])
            if group.count() != 0:
                group = group.get()
            else:
                group = title.split(' - ')[0]
            # 登録
            if tag in 'video':
                Video.objects.create(title = title, path = file, episode = episode, url = url, group = group)
            elif tag in 'adult':
                Adult.objects.create(title = title, path = file, episode = episode, url = url, group = group)

    except Exception as e:
        print(e)
# 一覧
def retriveVideo(tag):
    if 'video' in tag:
        videos = Video.objects.filter(process__isnull=True).\
            values('group').\
                annotate(last_episode=Min('episode'),last_id=Min('id')).\
                    values('last_id',"group", "last_episode")
    elif 'adult' in tag:
        videos = Adult.objects.filter(process__isnull=True).\
        values('group').\
            annotate(last_episode=Min('episode'),last_id=Min('id')).\
                values('last_id',"group", "last_episode")
    return videos
# 処理
def process(tag, id, process):
    if tag in 'video':
        video = Video.objects.get(id__exact=id)
    elif tag in 'adult':
        video = Adult.objects.get(id__exact=id)
    video.process = process
    video.save()
# 視聴
def watchVideo(process, id):
    if process in 'video':
        return Video.objects.get(id__exact=id)
    elif process in 'adult':
        return Adult.objects.get(id__exact=id)
# 次を視聴
def next(tag, id):
    if tag in 'video':
        video = Video.objects.get(id__exact=id)
        next_video = Video.objects.filter(id=id+1, group=video.group).first()
    elif tag in 'adult':
        video = Video.objects.get(id__exact=id)
        next_video = Video.objects.filter(id=id+1, group=video.group).first()
    if next_video:
        return next_video
    else:
        return None