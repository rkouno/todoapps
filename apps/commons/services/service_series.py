# util
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models.functions import Cast
from django.db.models import IntegerField

# django db
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.db.models import Count

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
def retriveGeneral(text, sort, cbxGenrue, cbxStatus, cbxRead):
    # ソート
    if sort == 10:   
        # 名前（昇順）
        orderby=('series',)
    elif sort == 11:   
        # 名前（降順）
        orderby=('-series',)
    elif sort == 20:
        # 状態（昇順）
        orderby=('maxStatus',)
    elif sort == 21:
        # 状態（降順）
        orderby=('-maxStatus',)
    elif sort == 30:
        # 確認日（昇順）
        orderby=('dtConfirm',)
    elif sort == 31:
        # 確認日（降順）
        orderby=('-dtConfirm',)
    elif sort == 40:
        # 直近ダウンロード（昇順）
        orderby=('dtLast',)
    elif sort == 41:
        # 直近ダウンロード（降順）
        orderby=('-dtLast',)
    else:
        # 確認日（降順）
        orderby=('dtConfirm',)
    orderby = orderby + ('series', 'maxslug')

    genrue = Q(info__genrue_id = cbxGenrue) if cbxGenrue else Q()
    status = Q(status = cbxStatus) if cbxStatus else Q()
    read   = Q(info__book__read_flg=cbxRead) if cbxRead else Q()
    search = Q(series_name__icontains = text) if text else Q()

    series = Series.objects.prefetch_related('info').exclude(info__book=None).filter((Q()), genrue, search, status, read).\
        annotate(series=Max('series_name'), 
                 maxslug=Max('slug'), 
                 dtLast=Max('info__book__regist_date'), 
                 readed=Min(Cast('info__book__read_flg', output_field=IntegerField())), 
                 dtConfirm=Max('confirm_date'), 
                 maxStatus=Max('status_id__status_name'),
                 maxVol=Count('info__book__volume')
                 ).\
            values('series', 'maxslug', 'maxStatus', 'dtConfirm', 'dtLast', 'maxVol').\
                order_by(*orderby)
    
    return series
# 一覧（成年コミック・成年小説）
def retriveHentai(text, sort, cbxCategory, cbxRead):
    if sort == 0:
        # 直近ダウンロード
        orderby=('readed', '-dtLast', 'series', 'maxslug')
    elif sort == 1:   
        # 名前
        orderby=('series', 'maxslug')
    elif sort == 2:
        # 確認日
        orderby=('-dtConfirm','series', 'maxslug')

    category = Q(info__book__category__category__icontains = cbxCategory) if cbxCategory else Q()
    read = Q(info__book__read_flg = cbxRead) if cbxRead else Q()    
    search = Q(series_name__icontains = text) if text else Q()
    series = Series.objects.prefetch_related('info').exclude(info__book=None).filter((Q(info__genrue_id = 3) | Q(info__genrue_id = 4)), search, category, read).\
        annotate(series=Max('series_name'), 
                 maxslug=Max('slug'), 
                 dtLast=Max('info__book__regist_date'), 
                 readed=Min(Cast('info__book__read_flg', output_field=IntegerField())), 
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
