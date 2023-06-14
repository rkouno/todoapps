from ast import keyword
from statistics import mode
from tabnanny import verbose
from tokenize import group
from django import template
from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.commons.const import appconst

# Create your models here.
class Period(models.Model):
    year        = models.IntegerField(verbose_name='年')
    period      = models.IntegerField(verbose_name='期')
    season      = models.CharField(max_length=2, verbose_name='季節')

class Anime(models.Model):
    title       = models.CharField(max_length = 255, blank=True, null=True, verbose_name='Title')
    keyword     = models.CharField(max_length = 255, blank=True, null=True, verbose_name='Search torrent word')
    isEnd       = models.BooleanField(null=True)
    period      = models.ForeignKey(Period, on_delete=models.CASCADE)
    dtStart     = models.DateField(verbose_name='Broadcast start date')
    dtEnd       = models.DateField(verbose_name='Broadcast end date')
    dtUpdate    = models.DateTimeField(default=timezone.now)

    def update(self):
        self.dtUpdate = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Video(models.Model):
    path     = models.CharField(max_length = 255, blank=False, null=False, verbose_name='パス')
    title    = models.CharField(max_length = 255, blank=False, null=False, verbose_name='タイトル')
    episode  = models.CharField(max_length = 2,   blank=True,  null=True,  verbose_name='話数')
    group    = models.ForeignKey(Anime, on_delete=models.CASCADE) 
    url      = models.CharField(max_length = 255, blank=True,  null=True,  verbose_name='URL')
    process  = models.CharField(max_length = 20,  blank=True,  null=True,  verbose_name='処理')
    dtRegist = models.DateTimeField(default=timezone.now, verbose_name='登録日')

    def __str__(self):
        return self.title
    
    def link(self):
        return self.url.replace('localhost', appconst.IP_ADDRESS)
    
class Adult(models.Model):
    path     = models.CharField(max_length = 255, blank=False, null=False, verbose_name='パス')
    title    = models.CharField(max_length = 255, blank=False, null=False, verbose_name='タイトル')
    episode  = models.CharField(max_length = 2,   blank=True,  null=True,  verbose_name='話数')
    group    = models.CharField(max_length = 255, blank=True,  null=True,  verbose_name='グループ')
    url      = models.CharField(max_length = 255, blank=False, null=False, verbose_name='URL')
    process  = models.CharField(max_length = 20,  blank=True,  null=True,  verbose_name='処理')
    dtRegist = models.DateTimeField(default=timezone.now, verbose_name='登録日')
    dtRecent = models.DateTimeField(default=timezone.now, verbose_name='最近視聴')
    
    def __str__(self):
        return self.title
    
    def link(self):
        return self.url.replace('localhost', appconst.IP_ADDRESS)
    
class Torrent(models.Model):
    torrent_link = models.TextField(primary_key=True, verbose_name='Torrentリンク')
    title        = models.TextField(verbose_name='Torrent')
    dtRegist     = models.DateTimeField(default=timezone.now, verbose_name='登録日')
    
    def __str__(self):
        return self.title