# Generated by Django 4.1.2 on 2023-09-18 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adult',
            old_name='group',
            new_name='groups',
        ),
    ]
