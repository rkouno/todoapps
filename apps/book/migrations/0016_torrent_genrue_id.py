# Generated by Django 4.1.2 on 2022-12-11 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_rename_author_id_workbook_art_by_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrent',
            name='genrue_id',
            field=models.IntegerField(default=1),
        ),
    ]