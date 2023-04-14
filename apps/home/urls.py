# 新規作成
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_list, name='index'),
    path('shutdown/', views.shutdown, name='shutdown'),
    path('sleep/', views.sleep, name='sleep'),
]