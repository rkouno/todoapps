# Generated by Django 3.2.15 on 2022-10-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0016_auto_20221009_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='process',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='処理'),
        ),
    ]