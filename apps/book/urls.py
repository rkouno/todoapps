# 新規作成
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_list, name='create_list'),
    path('process/', views.book_process, name='book_process'),
    path('edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('bookInfo/', views.book_info, name='book_info'),

    path('comic', views.book_comic, name='book_comic'),
    path('novel', views.book_novel, name='book_novel'),
    path('adult', views.book_adult, name='book_adult'),
    path('revice', views.book_revice, name='book_revice'),
    path('fix/<int:pk>', views.book_fix, name='book_fix'),
    path('detail/<slug:alias>/<int:pk>', views.book_detail, name='book_detail'),
    path('bookdownload/<slug:pk>', views.book_download, name='book_download'),
    
    path('adultlist/', views.adult_list, name='adult_list'),
    path('webscraping/', views.adult_webscraping, name='adult_webscraping'),
    path('download/<slug:pk>/', views.adult_download, name='adult_download'),
]