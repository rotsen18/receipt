# Generated by Django 4.2.1 on 2023-05-13 18:58

import gdstorage.storage
from django.db import migrations, models

import culinary.models


class Migration(migrations.Migration):
    dependencies = [
        ('culinary', '0022_delete_receiptimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='photo',
            field=models.ImageField(
                blank=True,
                null=True,
                storage=gdstorage.storage.GoogleDriveStorage(),
                upload_to=culinary.models.upload_receipt_photo,
                verbose_name='Photo'
                ),
        ),
    ]