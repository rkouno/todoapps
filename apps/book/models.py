from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import pykakasi

# ジャンル
class Genrue(models.Model):
    genrue_id   = models.IntegerField(primary_key=True, verbose_name='ジャンルID')
    genrue_name = models.CharField(max_length=10, verbose_name='ジャンル')

# ステータス
class Status(models.Model):
    status_id   = models.IntegerField(primary_key=True, verbose_name='ステータスID')
    status_name = models.CharField(max_length=4, verbose_name='ステータス')

# シリーズ
class Series(models.Model):
    series_id   = models.IntegerField(primary_key=True, verbose_name='シリーズID')
    series_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='ステータス名')
    nyaa_keyword= models.CharField(max_length=255, blank=True,  null=True, verbose_name='Torrent検索')
    status      = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='状態')
    confirm_date= models.DateField(default=timezone.now, verbose_name='確認日')

# 作者
class Author(models.Model):
    author_id   = models.IntegerField(primary_key=True, verbose_name='作者ID')
    author_name = models.CharField(max_length=255, verbose_name='作者名')
    genrue      = models.ForeignKey(Genrue, on_delete=models.CASCADE, verbose_name='ジャンル')

# パス
class Path(models.Model):
    genrue    = models.OneToOneField(Genrue, on_delete=models.CASCADE, primary_key=True, verbose_name='ジャンル')
    path      = models.CharField(max_length=255, blank=False, null=False, verbose_name='パス')

# 書籍情報
class Info(models.Model):
    book_id     = models.IntegerField(primary_key=True, verbose_name='書籍ID')
    genrue      = models.ForeignKey(Genrue, on_delete=models.CASCADE, verbose_name='ジャンル')
    story_by    = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='story_by_id', verbose_name='原作者')
    art_by      = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True, related_name='art_by_id', verbose_name='作画')
    title       = models.CharField(max_length=255, blank=False, null=False, verbose_name='タイトル')
    sub_title   = models.CharField(max_length=255, blank=True, null=True, verbose_name='サブタイトル')
    series      = models.ForeignKey(Series, on_delete=models.CASCADE, verbose_name='シリーズ')
    status      = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='ステータス')
    save_path   = models.ForeignKey(Path, on_delete=models.CASCADE, verbose_name='保存先')

# 書籍
class Book(models.Model):
    genrue      = models.ForeignKey(Genrue, on_delete=models.CASCADE, verbose_name='ジャンル')
    book        = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name='書籍情報')
    series      = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='book')
    book_name   = models.CharField(max_length=255, verbose_name='書籍名')
    file_path   = models.CharField(primary_key=True, max_length=255, verbose_name='ファイルパス')
    volume      = models.CharField(max_length=3, blank=True, null=True, verbose_name='巻数')
    read_flg    = models.BooleanField(default=False, verbose_name='既読フラグ')
    regist_date = models.DateTimeField(default=timezone.now, verbose_name='登録日')
    isPdf       = models.BooleanField(default=True)
    slug        = models.SlugField(unique=True, max_length=255)
   
    def __str__(self):
        return self.book_name

    def save(self, *args, **kwargs):
        if not self.slug:
            kks = pykakasi.kakasi()
            self.slug = slugify(''.join([item['hepburn'] for item in kks.convert(self.file_path)]))
        return super().save(*args, **kwargs)
    

class Workbook(models.Model):
    process     = models.CharField(max_length=10, blank=True, null=True)
    path        = models.CharField(max_length=255)
    name        = models.CharField(max_length=255, blank=True, null=True)
    genrue_id   = models.IntegerField(default=1)
    genrue_name = models.CharField(max_length=20, blank=True, null=True, error_messages="20文字以下で入力してください。")
    story_by_id = models.IntegerField(null=True)
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
    series       = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    adult_flg    = models.BooleanField(default=False)

    def update(self):
        self.regist_date = timezone.now()
        self.save()

class Image(models.Model):
    img_link = models.CharField(max_length=255)
    path     = models.CharField(max_length=255)
    def __str__(self):
        return self.img_link