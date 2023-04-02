from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from telegram import PhotoSize

from mixins.models import NameABC, DateTimesABC, AuthorABC


class Receipt(NameABC, DateTimesABC, AuthorABC):
    description = models.TextField(_('Description'))
    main_cooking_principe = models.ForeignKey(
        'directory.CookingType',
        verbose_name=_('main_cooking_principles'),
        on_delete=models.CASCADE,
        null=True
    )
    procedure = models.TextField(_('Procedure'), blank=True, default='')
    devices = models.ManyToManyField('directory.Device', verbose_name=_('Devices'))
    category = models.ForeignKey(
        'directory.CulinaryCategory',
        verbose_name=_('Category'),
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    source_link = models.URLField(_('Source_link'), null=True)
    receipt_portions = models.IntegerField(_('Receipt_portions'), validators=[MinValueValidator(limit_value=1)])
    estimate_time = models.DurationField(_('Estimate_time'), null=True)

    class Meta:
        verbose_name = _('Receipt')
        verbose_name_plural = _('Receipts')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    @property
    def raking(self):
        return round(self.comments.aggregate(avg=Avg('rate')).get('avg'), 1)


class ReceiptComponent(models.Model):
    receipt = models.ForeignKey(Receipt, verbose_name=_('Receipt'), on_delete=models.CASCADE, related_name='components')
    ingredient = models.ForeignKey('directory.Ingredient', verbose_name=_('Ingredient'), on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(
        'directory.MeasurementUnit',
        null=True,
        on_delete=models.CASCADE,
        related_name='receipts_components',
        verbose_name=_('Measurement_unit')
    )
    amount = models.FloatField(_('Amount'))

    def __str__(self):
        return f'{self.ingredient} - {self.amount} {self.measurement_unit}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.measurement_unit is None:
            self.user_measurement_unit = self.ingredient.default_measurement_unit
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _('ReceiptComponent')
        verbose_name_plural = _('ReceiptComponents')
        ordering = ['receipt']


class ReceiptComment(DateTimesABC, AuthorABC):
    class RateChoices(models.IntegerChoices):
        VERY_BAD = (1, 'very bad')
        BAD = (2, 'bad')
        NORMAL = (3, 'normal')
        GOOD = (4, 'good')
        PERFECT = (5, 'perfect')

    receipt = models.ForeignKey(Receipt, verbose_name=_('Receipt'), on_delete=models.CASCADE, related_name='comments')
    rate = models.IntegerField(_('Rate'), choices=RateChoices.choices, default=RateChoices.PERFECT)
    text = models.CharField(_('Text'), max_length=300, default='')

    def __str__(self):
        max_comment_length = 15
        text = f'{self.text[:max_comment_length]}...' if len(self.text) >= max_comment_length else self.text
        return f'{self.receipt}:{self.rate} {text}'

    class Meta:
        verbose_name = _('ReceiptComment')
        verbose_name_plural = _('ReceiptComments')
        ordering = ['-created_at']


class ReceiptImage(DateTimesABC):
    receipt = models.ForeignKey(Receipt, verbose_name=_('Receipt'), on_delete=models.CASCADE, related_name='photos')
    file_id = models.CharField(max_length=200)
    file_unique_id = models.CharField(max_length=20)
    file_size = models.IntegerField(null=True)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        verbose_name = _('ReceiptImage')
        verbose_name_plural = _('ReceiptImages')

    @property
    def photosize(self):
        return PhotoSize(self.file_id, self.file_unique_id, self.width, self.height, self.file_size)

    @property
    def image_url(self):
        file = self.photosize.get_file()
        return file.file_path
