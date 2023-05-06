# 新規作成
from django.urls import path
from . import views

urlpatterns = [
    # Download > 一覧
    path('sukebei/', views.download_sukebei, name='download_sukebei'),
    path('sukebei/webscrap', views.download_webscrap, name='download_webscrap'),
    path('sukebei/download/<int:pk>', views.download_sukebei_comic, name='download_sukebei_comic'),
    # Books > 一覧
    path('create/', views.workbook_create, name='workbook_create'),
    path('create/process/', views.workbook_process, name='workbook_process'),
    path('create/edit/<int:pk>/', views.workbook_edit, name='workbook_edit'),
    path('create/delete/<int:pk>/', views.workbook_delete, name='workbook_delete'),
    # Books > 編集
    path('create/edit/bookinfo/', views.book_info, name='book_info'),
    path('create/edit/delimage/', views.book_delimage, name='book_delimage'),
    # Master




    # path('bookInfo/', views.book_info, name='book_info'),
    # path('comic', views.book_comic, name='book_comic'),
    # path('novel', views.book_novel, name='book_novel'),
    # path('adult', views.book_adult, name='book_adult'),
    # path('revice', views.book_revice, name='book_revice'),
    # path('check/', views.book_check, name='book_check'),
    # path('fix/<slug:pk>', views.book_fix, name='book_fix'),
    # path('fix/<file>', views.book_none, name='book_none'),
    # path('detail/<slug:alias>/<pk>', views.book_detail, name='book_detail'),
    # # path('bookdownload/<slug:slug>', views.book_download, name='book_download'),
    # path('nyaa_download/', views.nyaa_download, name='nyaa_download'),
    # path('nyaa/<int:id>/<int:book_id>', views.nyaa, name='nyaa'),
    # path('nyaa/<int:id>/<int:book_id>', views.nyaa, name='nyaa'),
    # path('nyaa_download/download/<slug:alias>/<int:pk>', views.download, name='download'),
    # path('sukebe_download/', views.sukebe_download, name='sukebe_download'),
    # path('sukebe_download/download/<slug:alias>/<int:pk>', views.download, name='download'),
    # path('adultlist/', views.adult_list, name='adult_list'),
    # path('webscraping/', views.adult_webscraping, name='adult_webscraping'),
    # path('download/<slug:pk>/', views.adult_download, name='adult_download'),
]