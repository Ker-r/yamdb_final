from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'
    USER_STATUS = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
        (SUPERUSER, SUPERUSER)
    )

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Биография пользователя',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=USER_STATUS,
        default=USER,
        db_index=True,
        help_text='Права пользователя',
    )
    confirmation_code = models.TextField(
        verbose_name='Код подтверждения',
        help_text='Ваш код подтверждения полученный на почте',
        max_length=150,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def moderator(self):
        return self.role == self.MODERATOR

    @property
    def admin(self):
        return self.role == self.ADMIN

    @property
    def superuser(self):
        return self.role == self.SUPERUSER

    def __str__(self):
        return str(self.username)
