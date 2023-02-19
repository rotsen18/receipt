from django.db import models

from mixins.models import NameABC


class MeasurementUnit(NameABC):
    symbol = models.CharField(max_length=4, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Одиниця вимірювання'
        verbose_name_plural = 'Одиниці вимірювання'
        ordering = ['name']


class Ingredient(NameABC):
    description = models.CharField(max_length=255, blank=True, default='')
    default_measurement_unit = models.ForeignKey('directory.MeasurementUnit', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Інгредіент'
        verbose_name_plural = 'Інгредіенти'
        ordering = ['name']


class CulinaryCategory(NameABC):
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія в кулінарії'
        verbose_name_plural = 'Категорії в кулінарії'
        ordering = ['name']


class Device(NameABC):
    class DeviceTypeChoices(models.TextChoices):
        ELECTRIC = ('electric', 'different electric stuff')
        MANUAL = ('manual', 'devices for hand use only')

    device_type = models.CharField(max_length=10, choices=DeviceTypeChoices.choices)
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пристрій'
        verbose_name_plural = 'Пристрої'
        ordering = ['name']


class CookingType(NameABC):
    """Cooking preparing principe, ex.:bake."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Принципи проготування'
        verbose_name_plural = 'Принцип проготування'
        ordering = ['name']


class Category(NameABC):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='child_categories')
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name
