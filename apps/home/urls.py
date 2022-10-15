# 新規作成
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_list, name='index'),
]