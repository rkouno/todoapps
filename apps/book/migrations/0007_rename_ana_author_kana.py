# Generated by Django 4.1.2 on 2023-10-08 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_kana_author_ana'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='ana',
            new_name='kana',
        ),
    ]
