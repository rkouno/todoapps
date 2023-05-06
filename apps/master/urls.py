# 新規作成
from django.urls import path
from . import views

urlpatterns = [
  # hentai video
  path('adult/',views.adult_list, name='adult_list'),
  path('adult/edit/<int:id>',views.adult_edit, name='adult_edit'),
  # series
  path('series/',views.series_list, name='series_list'),
]