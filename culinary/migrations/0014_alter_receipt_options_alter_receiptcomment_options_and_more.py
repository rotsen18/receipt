# Generated by Django 4.1.7 on 2023-04-02 09:11

import django.core.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import receipt.middlewares


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('directory', '0003_alter_cookingtype_options_and_more'),
        ('culinary', '0013_receipt_estimate_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receipt',
            options={'ordering': ['name'], 'verbose_name': 'Receipt', 'verbose_name_plural': 'Receipts'},
        ),
        migrations.AlterModelOptions(
            name='receiptcomment',
            options={
                'ordering': ['-created_at'],
                'verbose_name': ('ReceiptComment',),
                'verbose_name_plural': ('ReceiptComments',)
            },
        ),
        migrations.AlterModelOptions(
            name='receiptcomponent',
            options={
                'ordering': ['receipt'],
                'verbose_name': 'ReceiptComponent',
                'verbose_name_plural': 'ReceiptComponents'
            },
        ),
        migrations.AlterModelOptions(
            name='receiptimage',
            options={'verbose_name': ('ReceiptImage',), 'verbose_name_plural': ('ReceiptImages',)},
        ),
        migrations.AlterField(
            model_name='receipt',
            name='author',
            field=models.ForeignKey(
                default=receipt.middlewares.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Author'
                ),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='directory.culinarycategory',
                verbose_name='Category'
                ),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='created_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text='Дата створення',
                verbose_name='Created_at'
                ),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='devices',
            field=models.ManyToManyField(to='directory.device', verbose_name='Devices'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='estimate_time',
            field=models.DurationField(null=True, verbose_name='Estimate_time'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='main_cooking_principe',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='directory.cookingtype',
                verbose_name='main_cooking_principles'
                ),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='modified_at',
            field=models.DateTimeField(
                auto_now=True,
                help_text='Дата останнього редагування',
                verbose_name='Modified_at'
                ),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='procedure',
            field=models.TextField(blank=True, default='', verbose_name='Procedure'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receipt_portions',
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(limit_value=1)],
                verbose_name='Receipt_portions'
                ),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='source_link',
            field=models.URLField(null=True, verbose_name='Source_link'),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='author',
            field=models.ForeignKey(
                default=receipt.middlewares.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Author'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='created_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text='Дата створення',
                verbose_name='Created_at'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='modified_at',
            field=models.DateTimeField(
                auto_now=True,
                help_text='Дата останнього редагування',
                verbose_name='Modified_at'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='rate',
            field=models.IntegerField(
                choices=[(1, 'very bad'), (2, 'bad'), (3, 'normal'), (4, 'good'), (5, 'perfect')],
                default=5,
                verbose_name='Rate'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='receipt',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='culinary.receipt',
                verbose_name='Receipt'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='text',
            field=models.CharField(default='', max_length=300, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='receiptcomponent',
            name='ingredient',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='directory.ingredient',
                verbose_name='Ingredient'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomponent',
            name='measurement_unit',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='receipts_components',
                to='directory.measurementunit',
                verbose_name='Measurement_unit'
                ),
        ),
        migrations.AlterField(
            model_name='receiptcomponent',
            name='receipt',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='components',
                to='culinary.receipt',
                verbose_name='Receipt'
                ),
        ),
        migrations.AlterField(
            model_name='receiptimage',
            name='created_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text='Дата створення',
                verbose_name='Created_at'
                ),
        ),
        migrations.AlterField(
            model_name='receiptimage',
            name='modified_at',
            field=models.DateTimeField(
                auto_now=True,
                help_text='Дата останнього редагування',
                verbose_name='Modified_at'
                ),
        ),
        migrations.AlterField(
            model_name='receiptimage',
            name='receipt',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='photos',
                to='culinary.receipt',
                verbose_name='Receipt'
                ),
        ),
    ]
