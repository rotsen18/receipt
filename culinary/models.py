from django.db import models
from django.db.models import Avg
from telegram import PhotoSize

from mixins.models import NameABC, DateTimesABC, AuthorABC


class Receipt(NameABC, DateTimesABC, AuthorABC):
    description = models.TextField()
    main_cooking_principe = models.ForeignKey('directory.CookingType', on_delete=models.CASCADE, null=True)
    procedure = models.TextField(blank=True, default='')
    devices = models.ManyToManyField('directory.Device')
    category = models.ForeignKey('directory.CulinaryCategory', on_delete=models.PROTECT, null=True, blank=True)
    source_link = models.URLField(null=True)
    receipt_portions = models.IntegerField()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепи'
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
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='components')
    ingredient = models.ForeignKey('directory.Ingredient', on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(
        'directory.MeasurementUnit',
        null=True,
        on_delete=models.CASCADE,
        related_name='receipts_components'
    )
    amount = models.FloatField()

    def __str__(self):
        return f'{self.ingredient} - {self.amount} {self.measurement_unit}'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.user_measurement_unit is None:
            self.user_measurement_unit = self.ingredient.default_measurement_unit
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'Складник рецепту'
        verbose_name_plural = 'Складники рецепту'
        ordering = ['receipt']


class ReceiptComment(DateTimesABC, AuthorABC):
    class RateChoices(models.IntegerChoices):
        VERY_BAD = (1, 'very bad')
        BAD = (2, 'bad')
        NORMAL = (3, 'normal')
        GOOD = (4, 'good')
        PERFECT = (5, 'perfect')

    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='comments')
    rate = models.IntegerField(choices=RateChoices.choices, default=RateChoices.PERFECT)
    text = models.CharField(max_length=300, default='')

    def __str__(self):
        max_comment_length = 15
        text = f'{self.text[:max_comment_length]}...' if len(self.text) >= max_comment_length else self.text
        return f'{self.receipt}:{self.rate} {text}'

    class Meta:
        verbose_name = 'Оцінка рецепту'
        verbose_name_plural = 'Оцінки рецепту'
        ordering = ['-created_at']


class ReceiptImage(DateTimesABC):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='photos')
    file_id = models.CharField(max_length=200)
    file_unique_id = models.CharField(max_length=20)
    file_size = models.IntegerField(null=True)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    @property
    def photosize(self):
        return PhotoSize(self.file_id, self.file_unique_id, self.width, self.height, self.file_size)

    @property
    def image_url(self):
        file = self.photosize.get_file()
        return file.file_path
