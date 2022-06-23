from datetime import datetime
from enum import Enum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class UserRole(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    @staticmethod
    def get_max_length():
        max_length = max(len(role.value) for role in UserRole)
        return max_length

    @staticmethod
    def get_all_roles():
        return tuple((r.value, r.name) for r in UserRole)


class User(AbstractUser):
    USERNAME_VALIDATOR = RegexValidator(r'^[\w.@+-]+\Z')
    bio = models.TextField(
        'Дополнительная информация',
        blank=True,
    )
    username = models.CharField(validators=[USERNAME_VALIDATOR],
                                max_length=150, unique=True)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(blank=True, max_length=124)
    confirmation_code = models.CharField(max_length=120, default='000000')
    role = models.CharField(
        max_length=UserRole.get_max_length(),
        choices=UserRole.get_all_roles(),
        default=UserRole.USER.value
    )
    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель Категории"""
    SLUG_VALIDATOR = RegexValidator(r'^[-a-zA-Z0-9_]+$')
    name = models.CharField(
        verbose_name='Название категории', max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50, unique=True,
        validators=[SLUG_VALIDATOR])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанры"""
    SLUG_VALIDATOR = RegexValidator(r'^[-a-zA-Z0-9_]+$')
    name = models.CharField(
        verbose_name='Название жанра', max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50, unique=True,
        validators=[SLUG_VALIDATOR])

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведения"""
    name = models.CharField(
        verbose_name='Название произведения', max_length=256)
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(
                0, message='Только из нашей эры!'),
            MaxValueValidator(
                datetime.now().year, message='Будущее временно не дочтупно')])
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category, related_name='title', blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Промежуточная модель для реализации отношения многие ко многим"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('date pablished', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('date pablished', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ['pub_date']
