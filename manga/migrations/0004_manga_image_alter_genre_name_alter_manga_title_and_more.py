# Generated by Django 4.1.4 on 2022-12-22 16:36

from django.db import migrations, models
import manga.utils


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0003_review_manga'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='image',
            field=models.ImageField(default=1, upload_to=manga.utils.manga_photo_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='manga',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Type'),
        ),
    ]
