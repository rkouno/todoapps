# Generated by Django 4.1.2 on 2023-04-20 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0061_alter_info_series'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='series_id',
        ),
    ]
