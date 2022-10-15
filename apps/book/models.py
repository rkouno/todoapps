from email.policy import default

from django.db import models


# Create your models here.
class Workbook(models.Model):
    process=models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    genrue_id = models.IntegerField(default=1)
    genrue_name = models.CharField(max_length=255, blank=True, null=True)
    author_id = models.IntegerField(null=True)
    story_by = models.CharField(max_length=255, blank=True, null=True)
    art_by = models.CharField(max_length=255, blank=True, null=True)
    book_id = models.IntegerField(null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    volume = models.IntegerField(null=True)
    book_name = models.CharField(max_length=255, blank=True, null=True)
    save_path = models.CharField(max_length=255, blank=True, null=True)
    exist_flg = models.BooleanField()
    
    def __str__(self):
        return self.path

class Torrent(models.Model):
    title = models.TextField()
    torrent_link = models.TextField(blank=True, null=True)
    img_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title