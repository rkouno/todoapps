# Generated by Django 4.1.2 on 2023-04-08 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0047_rename_series_id_book_series_remove_author_genrue_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='art_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='art_by_id', to='book.author', verbose_name='作画'),
        ),
    ]