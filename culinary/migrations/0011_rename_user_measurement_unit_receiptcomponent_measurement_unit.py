# Generated by Django 4.1.7 on 2023-03-25 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('culinary', '0010_auto_20230325_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receiptcomponent',
            old_name='user_measurement_unit',
            new_name='measurement_unit',
        ),
    ]