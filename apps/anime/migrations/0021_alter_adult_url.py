# Generated by Django 4.1.2 on 2022-11-05 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0020_anime_isend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adult',
            name='url',
            field=models.CharField(max_length=255, verbose_name='URL'),
        ),
    ]
