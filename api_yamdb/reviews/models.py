from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=200)
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Genre(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=200)
    slug = models.SlugField(verbose_name="Ссылка", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["id"]


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Название произведения",
    )
    year = models.IntegerField(
        verbose_name="Год произведения",
        validators=[validate_year],
    )
    description = models.TextField(
        default="-пусто-",
        blank=True,
        verbose_name="Описание произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name="Жанр произведения",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория произведения",
        related_name="titles_category",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]


class Review(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор отзыва",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name="Название произведения",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(
        verbose_name="Оценка произведения",
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["pub_date"]
        constraints = [
            models.UniqueConstraint(fields=["author", "title"],
                                    name="unique_review"
                                    ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор комментария",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(verbose_name="Текст комментария")
    pub_date = models.DateTimeField(
        verbose_name="Дата комментария",
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name="Отзыв",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["pub_date"]
