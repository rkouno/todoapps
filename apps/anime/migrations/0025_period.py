# Generated by Django 4.1.2 on 2023-03-16 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0024_adult_dtregist_video_dtregist_alter_torrent_dtregist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('yearmonth', models.IntegerField(primary_key=True, serialize=False, verbose_name='年月')),
                ('year', models.IntegerField(verbose_name='年')),
                ('period', models.IntegerField(verbose_name='期')),
                ('season', models.CharField(max_length=2, verbose_name='季節')),
            ],
        ),
    ]