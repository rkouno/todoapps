# Generated by Django 4.1.2 on 2023-01-14 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_torrent_genrue_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AlterField(
            model_name='book',
            name='file_path',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
