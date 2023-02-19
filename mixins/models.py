from django.conf import settings
from django.db import models
from django.utils import timezone

from receipt.middlewares import get_current_authenticated_user


class NameABC(models.Model):
    name = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        abstract = True


class DateTimesABC(models.Model):
    created_at = models.DateTimeField(default=timezone.now, help_text='Дата створення')
    modified_at = models.DateTimeField(auto_now=True, help_text='Дата останнього редагування')

    class Meta:
        abstract = True
        ordering = ['-created_at', '-modified_at']


class AuthorABC(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        default=get_current_authenticated_user,
    )

    class Meta:
        abstract = True
