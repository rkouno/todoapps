# Generated by Django 4.1.2 on 2023-10-01 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_delete_storyby_remove_author_author_id_author_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='book_id',
        ),
        migrations.AddField(
            model_name='info',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
