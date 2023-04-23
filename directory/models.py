from django.db import models
from django.utils.translation import gettext_lazy as _

from mixins.models import NameABC


class MeasurementUnit(NameABC):
    symbol = models.CharField(_('Symbol'), max_length=4, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('MeasurementUnit')
        verbose_name_plural = _('MeasurementUnits')
        ordering = ['name']


class Ingredient(NameABC):
    description = models.CharField(_('Description'), max_length=255, blank=True, default='')
    default_measurement_unit = models.ForeignKey(
        'directory.MeasurementUnit',
        verbose_name=_('MeasurementUnit'),
        on_delete=models.SET_NULL,
        null=True
    )
    product_url = models.URLField(_('Product_url'), null=True)
    product_data = models.JSONField(_('Product_data'), blank=True, null=True, default=dict)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ['name']


class Device(NameABC):
    class DeviceTypeChoices(models.TextChoices):
        ELECTRIC = ('electric', 'different electric stuff')
        MANUAL = ('manual', 'devices for hand use only')

    device_type = models.CharField(_('Device_type'), max_length=10, choices=DeviceTypeChoices.choices)
    description = models.CharField(_('Description'), max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        ordering = ['name']


class CookingType(NameABC):
    """Cooking preparing principe, ex.:bake."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('CookingType')
        verbose_name_plural = _('CookingTypes')
        ordering = ['name']


class CulinaryCategory(NameABC):
    parent = models.ForeignKey(
        'self',
        verbose_name=_('CulinaryCategory'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='child_categories'
    )
    description = models.CharField(_('Description'), max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('CulinaryCategory')
        verbose_name_plural = _('CulinaryCategories')
        ordering = ['name']


class ReceiptComponentsType(NameABC):
    """Component type, ex.: main, additional, etc."""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ReceiptType')
        verbose_name_plural = _('ReceiptTypes')
        ordering = ['name']
