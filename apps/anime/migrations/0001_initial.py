# Generated by Django 3.2.15 on 2022-09-19 14:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('keyword', models.TextField()),
                ('dtStart', models.DateTimeField(blank=True, null=True)),
                ('dtEnd', models.DateTimeField(blank=True, null=True)),
                ('dtUpdate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
