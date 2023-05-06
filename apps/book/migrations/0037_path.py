# Generated by Django 4.1.2 on 2023-04-08 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0036_remove_info_art_by_remove_info_story_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('genrue_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.genrue')),
            ],
        ),
    ]
