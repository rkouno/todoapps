# Generated by Django 4.1.2 on 2023-04-16 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0058_alter_torrent_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.series', verbose_name='シリーズ名'),
        ),
    ]
