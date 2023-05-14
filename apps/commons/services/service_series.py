# util
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

# django db
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q

# db
from apps.book.models import Series
from apps.book.models import Status

def get(pk):
    series = Series.objects.get(pk=pk)
    return series

def getAll():
    return Series.objects.all()

# シリーズの取得
def getObject(pk):
    series = Series.objects.filter(slug=pk).first()
    Series.objects.filter(slug=pk).update(confirm_date = timezone.now())
    return series

# 一覧（一般コミック・一般小説）
def retriveGeneral(text, sort):
    if sort == 0:
        # 直近ダウンロード
        orderby=('readed', '-dtLast', 'series', 'maxslug')
    elif sort == 1:   
        # 名前
        orderby=('series', 'maxslug')
    elif sort == 2:
        # 確認日
        orderby=('-maxStatus', 'dtConfirm', 'series', 'maxslug')
    search = Q(series_name__icontains = text) if text else Q()
    series = Series.objects.prefetch_related('info').filter((Q(info__genrue_id = 1) | Q(info__genrue_id = 2)), search).\
        annotate(series=Max('series_name'), 
                 maxslug=Max('slug'), 
                 dtLast=Max('info__book__regist_date'), 
                 readed=Min('info__book__read_flg'), 
                 dtConfirm=Max('confirm_date'), 
                 maxStatus=Max('status_id__status_name')).\
            values('series', 'maxslug', 'maxStatus', 'dtConfirm', 'dtLast').\
                order_by(*orderby)
    return series
# 一覧（成年コミック・成年小説）
def retriveHentai(text, sort):
    if sort == 0:
        # 直近ダウンロード
        orderby=('readed', '-dtLast', 'series', 'maxslug')
    elif sort == 1:   
        # 名前
        orderby=('series', 'maxslug')
    elif sort == 2:
        # 確認日
        orderby=('-dtConfirm','series', 'maxslug')
    search = Q(series_name__icontains = text) if text else Q()
    series = Series.objects.prefetch_related('info').filter((Q(info__genrue_id = 3) | Q(info__genrue_id = 4)), search).\
        annotate(series=Max('series_name'), 
                 maxslug=Max('slug'), 
                 dtLast=Max('info__book__regist_date'), 
                 readed=Min('info__book__read_flg'), 
                 dtConfirm=Max('confirm_date')).\
            values('series', 'maxslug', 'dtConfirm', 'dtLast').\
                order_by(*orderby)
    return series

# 登録
@transaction.atomic
def series_commit(series_name):
    try:
        series = get_object_or_404(Series, pk=series_name)
    except Exception as e:
        series = Series.objects.create(
            series_name  = series_name.strip(),
            nyaa_keyword = series_name.strip(),
            status_id    = 0,
        )
    return series

def retriveSeries(flg, text):
    search = Q(series_name__icontains = text) if text else Q()
    if flg:
        filter = Q((Q(info__genrue_id = 1) | Q(info__genrue_id = 2)), search)
    else:
        filter = Q((Q(info__genrue_id = 3) | Q(info__genrue_id = 4)), search)
    series = Series.objects.prefetch_related('info')\
        .filter(filter)\
            .annotate(name=Max('series_name'))\
                .order_by('status','name')
    return series

def seriesList(genrue_id):
    return Series.objects.all().order_by('series_name')
"""
master
"""
class master:
    def getObjects(slug):
        series = Series.objects.filter(slug=slug).first()
        return series
    
    def commit(name, series_name, nyaa_keyword, status):
        series = Series.objects.get(pk=name)
        series.series_name  = series_name.strip()
        series.nyaa_keyword = nyaa_keyword.strip()
        series.status       = Status.objects.get(pk=status)
        series.save()

    def delete(series_name):
        Series.objects.get(pk=series_name).delete()
    
    def del_raw_series(sql):
        for series in Series.objects.raw(sql):
            master.delete(series.series_name)
