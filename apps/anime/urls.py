from django.urls import path

from . import views

# 新規作成
urlpatterns = [
    # ダウンロード
    path('', views.anime_list, name='anime_list'),
    path('new/', views.anime_new, name='anime_new'),
    path('edit/<int:pk>', views.anime_edit, name='anime_edit'),
    # 一覧
    path('video/<int:sort_code>', views.video_index, name='video_index'),
    path('video/regist/', views.video_list, name='video_list'),
    path('hentai/<int:sort_code>', views.hentai_index, name='hentai_index'),
    path('hentai/regist/', views.hentai_list, name='hentai_list'),
    # 視聴
    path('video/watch/<int:id>/<tag>', views.video_watch, name='video_watch'),
    path('video/download/<int:id>/<tag>', views.video_download, name='video_download'),
    path('video/delete/<int:id>/<tag>', views.video_delete, name='video_delete'),
]