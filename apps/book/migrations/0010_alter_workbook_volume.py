# Generated by Django 4.1.2 on 2022-11-26 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_alter_workbook_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workbook',
            name='volume',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]