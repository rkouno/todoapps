# Generated by Django 3.2.15 on 2022-10-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0009_auto_20221001_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torrent',
            name='id',
        ),
        migrations.AlterField(
            model_name='torrent',
            name='torrent_link',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]