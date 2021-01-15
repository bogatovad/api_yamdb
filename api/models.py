from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(_('email'), unique=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='user')


User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField(verbose_name='название', max_length=200,
                            unique=True)
    year = models.IntegerField(
        verbose_name='год',
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        verbose_name='рейтинг',
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=2000,
        blank=True,
    )
    genre = models.ManyToManyField(
        to=Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанры',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


class Review(models.Model):
    title_id = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='id произведения',
    )
    text = models.TextField(verbose_name='текст', max_length=2000)
    score = models.IntegerField(
        verbose_name='оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(verbose_name='дата', auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.pub_date}: {self.text[:50]}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title_id'), name='review already exists',
            ),
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='id отзыва',
    )
    text = models.TextField(verbose_name='текст', max_length=500)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(verbose_name='дата', auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.pub_date}: {self.text[:50]}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

