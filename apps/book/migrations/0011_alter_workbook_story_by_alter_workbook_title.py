# Generated by Django 4.1.2 on 2022-12-04 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_alter_workbook_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workbook',
            name='story_by',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='workbook',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
