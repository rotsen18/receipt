# Generated by Django 4.1.7 on 2023-03-05 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culinary', '0004_alter_receiptcomment_options_receiptcomment_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='source_link',
            field=models.URLField(null=True),
        ),
    ]
