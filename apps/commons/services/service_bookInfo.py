# util
from django.db import transaction

# db
from django.db.models import Q
from apps.book.models import Info
from apps.book.models import Path
from apps.book.models import Author

"""
Book
"""
# シリーズ一覧
def getObject(series_id):
    infos = Info.objects.filter(series=series_id).first()
    return infos
# 書籍情報リストの取得
def searchBookInfo(genrue_id, title, sub_title):
    if sub_title:
        search = Q(genrue_id=genrue_id, title__icontains=title, sub_title__icontains=sub_title)
    else:
        search = Q(genrue_id=genrue_id, title__icontains=title)
    bi = Info.objects.filter(search).select_related('story_by_id').all().\
        values('title', 'sub_title', 'story_by__author_name', 'art_by__author_name')
    return bi
# ジャンルの取得
def getGenrueId(book_id):
    return Info.objects.filter(book_id=book_id).first().genrue.genrue_id
# 登録
@transaction.atomic
def info_commit(genrue_id, series_id, story_by_id, art_by_id, title, sub_title):
    info, created = Info.objects.get_or_create(
        genrue_id   = genrue_id,
        series_id   = series_id,
        story_by_id = Author.objects.get(pk=story_by_id).author_id,
        art_by_id   = Author.objects.get(pk=art_by_id).author_id,
        title       = title,
        sub_title   = sub_title,
        status_id   = 0,
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
