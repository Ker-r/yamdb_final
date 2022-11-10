from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name="titles", null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genres,
        related_name="titles"
    )
    name = models.CharField(max_length=256, db_index=True)
    year = models.PositiveSmallIntegerField(
        'Год выпуска', validators=(MaxValueValidator(date.today().year),),
        db_index=True, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв на произведение"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст отзыва',
        help_text='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        help_text='Автор',
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            [MinValueValidator(
                1, message='Оценка не может быть меньше 1'),
             MaxValueValidator(
                10, message='Оценка не может быть больше 10')]
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        help_text='Дата отзыва'
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                name="unique_review",
                fields=["title", "author"],
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарий к отзыву произведения"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата комментария',
        help_text='Дата комментария'
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
