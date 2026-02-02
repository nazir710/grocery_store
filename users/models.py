"""Модель пользователя и подписки."""


from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.constants import Constants


class MyUser(AbstractUser):

    username = models.CharField(
        max_length=Constants.username_max_length,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name='Уникальный юзернейм'
    )
    email = models.EmailField(
        max_length=Constants.email_max_length,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=Constants.first_name_max_length,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=Constants.last_name_max_length,
        verbose_name='Фамилия пользователя'
    )
    avatar = models.ImageField(
        upload_to='users/images/',
        null=True,
        default=''
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
