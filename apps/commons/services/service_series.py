# util
from django.db import transaction

# django db
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q

# db
from apps.book.models import Series

# シリーズの取得
def getObject(pk):
    series = Series.objects.get(pk=pk)
    return series

# 一覧（一般コミック・一般小説）
def retriveGeneral(text):
    search = Q(series_name__icontains = text) if text else Q()
    series = Series.objects.prefetch_related('book').filter((Q(book__genrue_id = 1) | Q(book__genrue_id = 2)), search).\
        annotate(id=Max('series_id'), series=Max('series_name'), dtLast=Max('book__regist_date'), readed=Min('book__read_flg')).\
            values('id', 'series').\
                order_by('readed', '-dtLast', 'series')
    return series
# 一覧（成年コミック・成年小説）
def retriveHentai(text):
    search = Q(series_name__icontains = text) if text else Q()
    series = Series.objects.prefetch_related('book').filter((Q(book__genrue_id = 3) | Q(book__genrue_id = 4)), search).\
        annotate(id=Max('series_id'), series=Max('series_name'), dtLast=Max('book__regist_date'), readed=Min('book__read_flg')).\
            values('id', 'series').\
                order_by('readed', '-dtLast', 'series')
    return series

# 登録
@transaction.atomic
def series_commit(series_name):
    series, created = Series.objects.get_or_create(
        series_name  = series_name,
        nyaa_keyword = series_name,
        status_id    = 0,
    )
    if created:
        series = Series.objects.filter(series_name=series_name).first()
    return series

def retriveSeries(flg):
    if flg:
        filter = Q(book__genrue_id = 1) | Q(book__genrue_id = 2)
    else:
        filter = Q(book__genrue_id = 3) | Q(book__genrue_id = 4)
    series = Series.objects.prefetch_related('book')\
        .filter(filter)\
            .annotate(name=Max('series_name'), id=Max('series_id'))\
                .order_by('name')
    return series