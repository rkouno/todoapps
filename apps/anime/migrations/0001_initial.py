# Generated by Django 4.1.2 on 2023-09-17 16:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('keyword', models.CharField(blank=True, max_length=255, null=True, verbose_name='Search torrent word')),
                ('isEnd', models.BooleanField(null=True)),
                ('dtStart', models.DateField(verbose_name='Broadcast start date')),
                ('dtEnd', models.DateField(verbose_name='Broadcast end date')),
                ('dtUpdate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Kana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kana', models.CharField(max_length=2, verbose_name='読み仮名')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='年')),
                ('period', models.IntegerField(verbose_name='期')),
                ('season', models.CharField(max_length=2, verbose_name='季節')),
            ],
        ),
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('torrent_link', models.TextField(primary_key=True, serialize=False, verbose_name='Torrentリンク')),
                ('title', models.TextField(verbose_name='Torrent')),
                ('dtRegist', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, verbose_name='パス')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('episode', models.CharField(blank=True, max_length=2, null=True, verbose_name='話数')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='URL')),
                ('process', models.CharField(blank=True, max_length=20, null=True, verbose_name='処理')),
                ('dtRegist', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.anime')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category', models.CharField(max_length=255, verbose_name='カテゴリ')),
                ('adult_flg', models.BooleanField(blank=True, null=True, verbose_name='アダルト')),
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False, verbose_name='カテゴリID')),
                ('kana', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.kana')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.period'),
        ),
        migrations.CreateModel(
            name='Adult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, verbose_name='パス')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('episode', models.CharField(blank=True, max_length=2, null=True, verbose_name='話数')),
                ('group', models.CharField(blank=True, max_length=255, null=True, verbose_name='グループ')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='評価')),
                ('process', models.CharField(blank=True, max_length=20, null=True, verbose_name='処理')),
                ('dtRegist', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('dtRecent', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最近視聴')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.category')),
            ],
        ),
    ]
