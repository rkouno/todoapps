# Generated by Django 4.1.2 on 2023-04-09 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0051_torrent_adult_flg_torrent_img_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrent',
            name='adult_flg',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]