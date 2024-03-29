# Generated by Django 4.1.7 on 2023-04-22 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('directory', '0005_receiptcomponentstype'),
        ('culinary', '0018_receiptcomment_telegram_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptcomponent',
            name='receipt_components_type',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='directory.receiptcomponentstype',
                verbose_name='Receipt_components_type'
                ),
        ),
    ]
