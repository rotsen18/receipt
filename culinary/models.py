from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from gdstorage.storage import GoogleDriveStorage

from mixins.models import AuthorABC, DateTimesABC, NameABC, TelegramUserABC

gd_storage = GoogleDriveStorage()


def upload_receipt_photo(instance, filename):
    return f'receipts/{instance.category.id}/{filename}'


class Receipt(NameABC, DateTimesABC, AuthorABC):
    description = models.TextField(_('Description'))
    main_cooking_principe = models.ForeignKey(
        'directory.CookingType',
        verbose_name=_('main_cooking_principles'),
        on_delete=models.CASCADE,
        null=True,
    )
    procedure = models.TextField(_('Procedure'), blank=True, default='')
    devices = models.ManyToManyField('directory.Device', verbose_name=_('Devices'))
    category = models.ForeignKey(
        'directory.CulinaryCategory',
        verbose_name=_('Category'),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    source_link = models.URLField(_('Source_link'), null=True)
    receipt_portions = models.IntegerField(_('Receipt_portions'), validators=[MinValueValidator(limit_value=1)])
    estimate_time = models.DurationField(_('Estimate_time'), null=True)
    photo = models.FileField(_('Photo'), upload_to=upload_receipt_photo, null=True, blank=True, storage=gd_storage)

    class Meta:
        verbose_name = _('Receipt')
        verbose_name_plural = _('Receipts')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    @property
    def raking(self):
        if not self.comments.exists():
            return ''
        return round(self.comments.aggregate(avg=Avg('rate')).get('avg'), 1)


class ReceiptComponent(models.Model):
    receipt = models.ForeignKey(Receipt, verbose_name=_('Receipt'), on_delete=models.CASCADE, related_name='components')
    receipt_components_type = models.ForeignKey(
        'directory.ReceiptComponentsType',
        verbose_name=_('Receipt_components_type'),
        on_delete=models.CASCADE,
        null=True,
    )
    ingredient = models.ForeignKey('directory.Ingredient', verbose_name=_('Ingredient'), on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(
        'directory.MeasurementUnit',
        null=True,
        on_delete=models.CASCADE,
        related_name='receipts_components',
        verbose_name=_('Measurement_unit'),
    )
    amount = models.FloatField(_('Amount'))

    class Meta:
        verbose_name = _('ReceiptComponent')
        verbose_name_plural = _('ReceiptComponents')
        ordering = ['receipt']

    def __str__(self):
        return f'{self.ingredient} - {self.amount} {self.measurement_unit}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None,
    ):
        if self.measurement_unit is None:
            self.user_measurement_unit = self.ingredient.default_measurement_unit
        super().save(force_insert, force_update, using, update_fields)


class ReceiptComment(DateTimesABC, AuthorABC, TelegramUserABC):
    class RateChoices(models.IntegerChoices):
        VERY_BAD = (1, 'very bad')
        BAD = (2, 'bad')
        NORMAL = (3, 'normal')
        GOOD = (4, 'good')
        PERFECT = (5, 'perfect')

    receipt = models.ForeignKey(Receipt, verbose_name=_('Receipt'), on_delete=models.CASCADE, related_name='comments')
    rate = models.IntegerField(_('Rate'), choices=RateChoices.choices, default=RateChoices.PERFECT)
    text = models.CharField(_('Text'), max_length=300, default='')

    class Meta:
        verbose_name = _('ReceiptComment')
        verbose_name_plural = _('ReceiptComments')
        ordering = ['-created_at']

    def __str__(self):
        max_comment_length = 15
        text = f'{self.text[:max_comment_length]}...' if len(self.text) >= max_comment_length else self.text
        return f'{self.receipt}:{self.rate} {text}'


class ReceiptSource(NameABC, DateTimesABC):
    receipt = models.ForeignKey(
        Receipt,
        verbose_name=_('Receipt'),
        on_delete=models.CASCADE,
        related_name='sources',
        null=True
    )
    source = models.TextField(verbose_name=_('Source'), default='')

    class Meta:
        verbose_name = _('ReceiptSource')
        verbose_name_plural = _('ReceiptSources')
