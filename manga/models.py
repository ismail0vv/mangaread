from django.db import models
from django.utils.text import slugify

from MangaRead.settings.settings import AUTH_USER_MODEL


# Create your models here.
class Genre(models.Model):
    """Жанр Манги"""
    name = models.CharField('Жанр', max_length=255)

    def __str__(self):
        return self.name


class Type(models.Model):
    """Тип манги"""
    name = models.CharField('Тип', max_length=255)

    def __str__(self):
        return self.name


class Manga(models.Model):
    """Манга"""

    title = models.CharField('Название', max_length=255)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name='mangas')
    genres = models.ManyToManyField(Genre, related_name='mangas')
    release_year = models.IntegerField()
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Manga, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    """Отзыв"""
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='reviews')
