# Generated by Django 4.1.7 on 2023-04-22 15:19

from django.db import migrations, models

import culinary.models


class Migration(migrations.Migration):
    dependencies = [
        ('culinary', '0019_receiptcomponent_receipt_components_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='photo',
            field=models.ImageField(null=True, upload_to=culinary.models.upload_receipt_photo, verbose_name='Photo'),
        ),
    ]