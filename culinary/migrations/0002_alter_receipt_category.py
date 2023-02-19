# Generated by Django 4.1.7 on 2023-02-19 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
        ('culinary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directory.category'),
        ),
    ]