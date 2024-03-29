# Generated by Django 4.1.7 on 2023-04-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('directory', '0004_alter_measurementunit_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptComponentsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'ReceiptType',
                'verbose_name_plural': 'ReceiptTypes',
                'ordering': ['name'],
            },
        ),
    ]
