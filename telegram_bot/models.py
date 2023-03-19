from django.conf import settings
from django.db import models


class TelegramUser(models.Model):
    class TypeUserChoice(models.TextChoices):
        ADMIN = ('Admin', 'Admin')
        CLIENT = ('Client', 'Client')

    type_user = models.CharField(max_length=15, choices=TypeUserChoice.choices, default=TypeUserChoice.CLIENT)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='telegram_user'
    )
    telegram_id = models.BigIntegerField(default=None, null=True, blank=True, verbose_name='ID юзера в телеграмi.')
    first_name = models.CharField(max_length=35, default='')
    last_name = models.CharField(max_length=35, null=True, default='')
    full_name = models.CharField(max_length=35, null=True, default='')
    name = models.CharField(max_length=35, null=True, default='')
    username = models.CharField(max_length=35, null=True, default='')

    @property
    def is_telegram_admin(self):
        return self.type_user == self.TypeUserChoice.ADMIN
