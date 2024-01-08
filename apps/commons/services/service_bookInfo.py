# util
from django.db import transaction
from django.db import connection

# db
from django.db.models import Q
from django.db.models import Max
from apps.book.models import Info
from apps.book.models import Path
from apps.book.models import Status

# service
from apps.commons.services import service_author as sa
from apps.commons.services import service_genrue as sg
from apps.commons.services import service_series as ss
from apps.commons.services.service_series import master as sm
"""
Book
"""
def get(pk):
    info = Info.objects.get(pk=pk)
    return info

def getAll():
    return Info.objects.all()

# 書籍情報リストの取得
def searchBookInfo(genrue_id, title, sub_title):
    if sub_title:
        search = Q(genrue_id=genrue_id, title__icontains=title, sub_title__icontains=sub_title)
    else:
        search = Q(genrue_id=genrue_id, title__icontains=title)
    bi = Info.objects.filter(search).select_related('story_by_id').all().\
        values('title', 'sub_title', 'story_by__author_name', 'art_by__author_name').\
            order_by('title', 'sub_title')
    return bi
# ジャンルの取得
def getGenrueId(id):
    return Info.objects.filter(id=id).first().genrue.genrue_id
# 登録
@transaction.atomic
def info_commit(genrue_id, series_id, story_by_id, art_by_id, title, sub_title):
    info, created = Info.objects.get_or_create(
        genrue_id   = genrue_id,
        series_id   = series_id,
        story_by_id = sa.get(story_by_id).id,
        art_by_id   = sa.get(art_by_id).id,
        title       = title,
        sub_title   = sub_title,
        save_path   = Path.objects.get(genrue_id=genrue_id),
    )
    if created:
        info = Info.objects.filter(
            genrue_id   = genrue_id, 
            series_id   = series_id, 
            story_by_id = story_by_id,
            art_by_id   = art_by_id,
            title       = title,
            sub_title   = sub_title
        ).first()
    return info
# 保存先の取得
def savePath(id):
    path = Path.objects.get(pk=id)
    return path.path

def rawObjects(sql, param):
    bi = Info.objects.raw(sql, param)
    return bi

# def rawObjects(sql):
#     bi = Info.objects.raw(sql)
#     return bi

def searchInfo(filter):
    infos = Info.objects.filter(filter)
    return infos

def getSeriesToGenrueId(series_name):
    genrue_id = Info.objects.filter(series_id=series_name).\
                    aggregate(genrue=Max('genrue_id'))
    return int(genrue_id['genrue'])

def delete(pk):
    Info.objects.get(pk=pk).delete()

"""
info
"""
class master:
    def retriveInfos(text, genrue_id):      
        filter=Q(title__icontains=text)|Q(sub_title__icontains=text) if text else Q()
        infos = Info.objects.filter(filter, genrue_id=genrue_id).\
            order_by('series__series_name', 'title', 'sub_title')

        return infos
    def update(form, genrue, story_by, art_by, title, sub_title, series, status, save_path):
        info = form.save(commit=False)
        info.genrue    = sg.getObject(genrue[0])
        info.story_by  = sa.get(story_by[0])
        info.art_by    = sa.get(art_by[0])
        info.title     = title.strip()
        info.sub_title = sub_title.strip()
        info.series    = ss.get(series[0])
        info.save_path = Path.objects.get(pk=save_path[0])
        info.status    = Status.objects.get(pk=status[0])
        info.save()
    
