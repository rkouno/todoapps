# Generated by Django 3.2.15 on 2022-09-25 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0003_anime_episode'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='lastEpisode',
            field=models.IntegerField(null=True, verbose_name='最新話'),
        ),
    ]