# Generated by Django 4.1.2 on 2023-08-16 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0034_alter_adult_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=1, max_length=255, primary_key=True, serialize=False, verbose_name='カテゴリID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adult',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.category'),
        ),
    ]