from django.db import models
from django.utils import timezone

class book(models.Model):
    genrue_id   = models.IntegerField()
    genrue_name = models.CharField(max_length=255)
    book_id     = models.IntegerField()
    story_by_id = models.IntegerField()
    story_by    = models.CharField(max_length=20, blank=False, null=False)
    art_by_id   = models.IntegerField()
    art_by      = models.CharField(max_length=20, blank=True, null=True)
    title       = models.CharField(max_length=50, blank=False, null=False)
    sub_title   = models.CharField(max_length=50, blank=True, null=True)
    book_name   = models.CharField(max_length=255)
    file_path   = models.CharField(max_length=255)
    volume      = models.CharField(max_length=3, blank=True, null=True)
    read_flg    = models.BooleanField(default=False)
    regist_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.book_name
    
class genrue(models.Model):
    genrue_id   = models.IntegerField(primary_key=True,)
    genrue_name = models.CharField(max_length=255)
    def __str__(self):
        return self.genrue_name

class status(models.Model):
    status_id   = models.IntegerField(primary_key=True,)
    status_name = models.CharField(max_length=255)
    def __str__(self):
        return self.status_name
    
class author(models.Model):
    author_id   = models.IntegerField(primary_key=True,)
    author_name = models.CharField(max_length=255)
    genrue_id   = models.CharField(max_length=255)
    
    def __str__(self):
        return self.author_name
    
class info(models.Model):
    book_id     = models.IntegerField(primary_key=True,)
    genrue      = models.ForeignKey(genrue, on_delete=models.CASCADE)
    story_by_id = models.IntegerField()
    story_by    = models.CharField(max_length=255, blank=False, null=True)
    art_by_id   = models.IntegerField()
    art_by      = models.CharField(max_length=255, blank=True, null=True)
    title       = models.CharField(max_length=255, blank=False, null=False)
    sub_title   = models.CharField(max_length=255, blank=True, null=True)
    save_path   = models.CharField(max_length=255, blank=True, null=True)
    status      = models.ForeignKey(status, on_delete=models.CASCADE)
    confirm_date= models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

class Workbook(models.Model):
    process     = models.CharField(max_length=10, blank=True, null=True)
    path        = models.CharField(max_length=255)
    name        = models.CharField(max_length=255, blank=True, null=True)
    genrue_id   = models.IntegerField(default=1)
    genrue_name = models.CharField(max_length=10, blank=True, null=True)
    story_by_id   = models.IntegerField(null=True)
    story_by    = models.CharField(max_length=20, blank=False, null=True)
    art_by      = models.CharField(max_length=20, blank=True, null=True)
    art_by_id   = models.IntegerField(null=True)
    book_id     = models.IntegerField(null=True)
    title       = models.CharField(max_length=50, blank=False, null=True)
    sub_title   = models.CharField(max_length=50, blank=True, null=True)
    volume      = models.CharField(max_length=5, blank=True, null=True)
    book_name   = models.CharField(max_length=255, blank=True, null=True)
    save_path   = models.CharField(max_length=255, blank=True, null=True)
    exist_flg   = models.BooleanField()
    
    def __str__(self):
        return self.path

class Torrent(models.Model):
    title        = models.TextField()
    torrent_link = models.TextField()
    img_link     = models.TextField(blank=True, null=True)
    downloaded   = models.BooleanField(default=False)
    regist_date  = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def update(self):
        self.regist_date = timezone.now()
        self.save()

class Image(models.Model):
    img_link = models.CharField(max_length=255)

    def __str__(self):
        return self.img_link