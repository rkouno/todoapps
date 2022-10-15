from ast import keyword
from statistics import mode
from tabnanny import verbose
from tokenize import group
from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Anime(models.Model):
    title = models.CharField(max_length = 255, verbose_name='Title')
    keyword = models.CharField(max_length = 255, blank=True, null=True, verbose_name='Search torrent word')
    dtStart = models.DateField(verbose_name='Broadcast start date')
    dtEnd = models.DateField(verbose_name='Broadcast end date')
    dtUpdate = models.DateTimeField(default=timezone.now)

    def update(self):
        self.dtUpdate = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Video(models.Model):
    path = models.CharField(max_length = 255, verbose_name='パス')
    title = models.CharField(max_length = 255, verbose_name='タイトル')
    episode = models.CharField(blank=True, null=True, max_length = 2, verbose_name='話数')
    group = models.CharField(blank=True, null=True, max_length = 255, verbose_name='グループ')
    url = models.CharField(blank=True, null=True, max_length = 255, verbose_name='URL')
    process = models.CharField(max_length = 20, blank=True, null=True, verbose_name='処理')

class Adult(models.Model):
    path = models.CharField(max_length = 255, verbose_name='パス')
    title = models.CharField(max_length = 255, verbose_name='タイトル')
    episode = models.CharField(blank=True, null=True, max_length = 2, verbose_name='話数')
    group = models.CharField(blank=True, null=True, max_length = 255, verbose_name='グループ')
    url = models.CharField(blank=True, null=True, max_length = 255, verbose_name='URL')
    process = models.CharField(max_length = 20, blank=True, null=True, verbose_name='処理')

class Torrent(models.Model):
    torrent_link = models.TextField(primary_key=True,verbose_name='Torrentリンク')
    title = models.TextField(verbose_name='Torrent')

    def __str__(self):
        return self.title