from django.urls import path

from . import views

# 新規作成
urlpatterns = [
    path('', views.anime_list, name='index'),
    path('new/', views.anime_new, name='anime_new'),
    path('edit/<int:pk>', views.anime_edit, name='anime_edit'),
    path('video/', views.video_index, name='video_index'),
    path('adultvideo/', views.adult_index, name='adult_index'),
    path('list/', views.video_list, name='video_list'),
    path('hentai/', views.hentai_list, name='hentai_list'),
    path('watch/<int:id>/<tag>', views.video_watch, name='video_watch'),
    path('download/<int:id>/<tag>', views.video_download, name='video_download'),
    path('delete/<int:id>/<tag>', views.video_delete, name='video_delete'),
]