# 新規作成
from django.urls import path
from . import views

urlpatterns = [
  # hentai video
  path('adult/',views.adult_list, name='adult_list'),
  path('adult/edit/<int:id>',views.adult_edit, name='adult_edit'),
  # series
  path('series/',views.series_list, name='series_list'),
  path('series/edit/<str:slug>',views.series_edit, name='series_edit'),
  # author
  path('author/',views.author_list, name='author_list'),
  path('author/edit/<int:author_id>',views.author_edit, name='author_edit'),
  # info
  path('info/',views.info_list, name='info_list'),
  path('info/edit/<int:book_id>',views.info_edit, name='info_edit'),
]