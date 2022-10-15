# 新規作成
from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('adult/', views.adult_list, name='adult_list'),
    path('create/', views.create_list, name='create_list'),
    path('webscraping/', views.adult_webscraping, name='adult_webscraping'),
    path('download/<int:pk>/', views.adult_download, name='adult_download'),
]