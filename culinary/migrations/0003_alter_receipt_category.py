# Generated by Django 4.1.7 on 2023-02-19 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
        ('culinary', '0002_alter_receipt_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directory.culinarycategory'),
        ),
    ]
