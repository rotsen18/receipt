from django.db import models
from django.db.models import Avg

from mixins.models import NameABC, DateTimesABC, AuthorABC


class Receipt(NameABC, DateTimesABC, AuthorABC):
    description = models.TextField()
    main_cooking_principe = models.ForeignKey('directory.CookingType', on_delete=models.CASCADE, null=True)
    procedure = models.TextField(blank=True, default='')
    devices = models.ManyToManyField('directory.Device')
    category = models.ForeignKey('directory.CulinaryCategory', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепи'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    @property
    def raking(self):
        return round(self.votes.aggregate(avg=Avg('rate')), 1)


class ReceiptComponent(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='components')
    ingredient = models.ForeignKey('directory.Ingredient', on_delete=models.CASCADE)
    user_measurement_unit = models.ForeignKey(
        'directory.MeasurementUnit',
        null=True,
        on_delete=models.CASCADE,
        related_name='receipts_components'
    )
    amount = models.FloatField()

    def __str__(self):
        return f'{self.ingredient} - {self.amount}{self.measurement_unit}'

    @property
    def measurement_unit(self):
        if self.user_measurement_unit:
            return self.user_measurement_unit
        elif self.ingredient.default_measurement_unit:
            return self.ingredient.default_measurement_unit
        return

    class Meta:
        verbose_name = 'Складник рецепту'
        verbose_name_plural = 'Складники рецепту'
        ordering = ['receipt']


class ReceiptVote(DateTimesABC, AuthorABC):
    class RateChoices(models.IntegerChoices):
        VERY_BAD = (1, 'very bad')
        BAD = (2, 'bad')
        NORMAL = (3, 'normal')
        GOOD = (4, 'good')
        perfect = (5, 'perfect')

    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='votes')
    rate = models.IntegerField(choices=RateChoices.choices)

    def __str__(self):
        return f'{self.receipt}: {self.rate}'

    class Meta:
        verbose_name = 'Оцінка рецепту'
        verbose_name_plural = 'Оцінки рецепту'
        ordering = ['-created_at']


class ReceiptComment(AuthorABC, DateTimesABC):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    def __str__(self):
        max_comment_length = 15
        return f'{self.text[:max_comment_length]}...' if len(self.text) >= max_comment_length else self.text

    class Meta:
        verbose_name = 'Комент'
        verbose_name_plural = 'Коменти'
        ordering = ['-created_at']
