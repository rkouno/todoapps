# 新規作成
from django.urls import path
from django.urls import register_converter
from . import views

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
    # Download > 一覧(Nyaa)
    path('nyaa/', views.nyaa_list, name='nyaa_list'),
    path('nyaa/webscrap', views.nyaa_webscrap, name='nyaa_webscrap'),
    path('nyaa/download/<url:pk>', views.nyaa_download, name='nyaa_download'),
    # Download > 一覧(Sukebei)
    path('sukebei/', views.sukebei_list, name='sukebei_list'),
    path('sukebei/webscrap', views.sukebei_webscrap, name='sukebei_webscrap'),
    path('sukebei/download/<url:pk>', views.sukebei_download, name='sukebei_download'),
    # Download > 一覧(Check)
    path('check/', views.check_list, name='check_list'),
    path('check/book', views.book_webscrap, name='book_webscrap'),
    path('check/booklist', views.book_list, name='book_list'),
    path('check/booklist/nyaa/<url:pk>', views.check_nyaa_download, name='check_nyaa_download'),
    path('check/booklist/sukebei/<url:pk>', views.check_sukebei_download, name='check_sukebei_download'),
    path('check/booklist/edit/<slug:pk>', views.check_edit, name='check_edit'),
    # Books > 一覧
    path('create/', views.workbook_create, name='workbook_create'),
    path('create/process/', views.workbook_process, name='workbook_process'),
    path('create/edit/<int:pk>/', views.workbook_edit, name='workbook_edit'),
    path('create/delete/<int:pk>/', views.workbook_delete, name='workbook_delete'),
    # Books > 編集
    path('create/edit/bookinfo/', views.book_info, name='book_info'),
    path('create/edit/delimage/', views.book_delimage, name='book_delimage'),
]

