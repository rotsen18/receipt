# Generated by Django 4.1.7 on 2023-02-19 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culinary', '0003_alter_receipt_category'),
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='culinarycategory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_categories', to='directory.culinarycategory'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
