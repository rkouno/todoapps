# 新規作成
from django.urls import path
from . import views

urlpatterns = [
    # 一覧(一般)
    path('general/', views.book_general, name='book_general'),
    # 一覧(成年成年)
    path('hentai/', views.book_hentai, name='book_hentai'),
    # 一覧 > シリーズ一覧
    path('series/<int:series_id>', views.book_series, name='book_series'),
    path('serieshentai/<int:series_id>', views.book_series_author, name='book_series_author'),
    # 一覧 > シリーズ一覧 > ダウンロード
    path('series/download/<slug:slug>', views.book_download, name='book_download'),
    # 一覧 > シリーズ一覧 > 編集
    path('edit/<slug:pk>', views.book_edit, name='book_edit'),
    # 一覧 > シリーズ一覧 > Nyaaリスト
    path('nyaa/<int:torrent_id>/<int:series_id>', views.book_nyaa, name='book_nyaa'),

    # 修正リスト
    path('revice/', views.book_revice, name='book_revice'),    
]