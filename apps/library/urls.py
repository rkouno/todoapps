# 新規作成
from django.urls import path
from . import views
from django.urls import register_converter

class path_converter:
    regex = '[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)\'\[\]]+'
    def to_python(self, value):
        str = f'https://{value}'
        return str
    def to_url(self, value):
        str = value.replace('https://', '')
        print(str)
        return str

register_converter(path_converter, 'url')

urlpatterns = [
    # 一覧(一般)
    path('general/<int:sort>', views.book_general, name='book_general'),
    # 一覧(成年成年)
    path('hentai/<int:sort>', views.book_hentai, name='book_hentai'),
    # 一覧 > シリーズ一覧
    path('series/<slug:slug>', views.book_series, name='book_series'),
    path('series/edit/<slug:slug>', views.book_series_edit, name='book_series_edit'),
    path('serieshentai/<slug:slug>', views.book_series_author, name='book_series_author'),
    # 一覧 > シリーズ一覧 > ダウンロード
    path('series/download/<slug:slug>', views.book_download, name='book_download'),
    # 一覧 > シリーズ一覧 > 編集
    path('edit/<slug:pk>', views.book_edit, name='book_edit'),
    # 一覧 > シリーズ一覧 > Nyaaリスト
    path('nyaa/<url:torrent_link>', views.book_nyaa, name='book_nyaa'),

    # 修正リスト
    path('revice/', views.book_revice, name='book_revice'),    
]