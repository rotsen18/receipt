# Generated by Django 4.1.7 on 2023-04-23 06:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('directory', '0005_receiptcomponentstype'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='product_url',
            field=models.URLField(null=True, verbose_name='Product_url'),
        ),
    ]