# Generated by Django 4.1.2 on 2023-03-19 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0027_anime_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.anime'),
        ),
    ]