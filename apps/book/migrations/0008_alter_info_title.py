# Generated by Django 4.1.2 on 2022-11-20 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_alter_info_story_by_alter_info_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]