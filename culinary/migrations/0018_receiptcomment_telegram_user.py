# Generated by Django 4.1.7 on 2023-04-15 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('telegram_bot', '0007_telegramuser_name_alter_telegramuser_username'),
        ('culinary', '0017_receiptsource_created_at_receiptsource_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptcomment',
            name='telegram_user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='telegram_user',
                to='telegram_bot.telegramuser',
                verbose_name='Telegram user'
                ),
        ),
    ]
