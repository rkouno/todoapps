# Generated by Django 4.1.2 on 2023-05-01 05:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0067_remove_torrent_id_alter_torrent_torrent_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrent',
            name='regist_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
