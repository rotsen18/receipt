# Generated by Django 4.1.7 on 2023-02-19 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CookingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={
                'verbose_name': 'Принципи проготування',
                'verbose_name_plural': 'Принцип проготування',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CulinaryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Категорія в кулінарії',
                'verbose_name_plural': 'Категорії в кулінарії',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('device_type', models.CharField(choices=[('electric', 'different electric stuff'), ('manual', 'devices for hand use only')], max_length=10)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Пристрій',
                'verbose_name_plural': 'Пристрої',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('symbol', models.CharField(blank=True, default='', max_length=4)),
            ],
            options={
                'verbose_name': 'Одиниця вимірювання',
                'verbose_name_plural': 'Одиниці вимірювання',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('default_measurement_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='directory.measurementunit')),
            ],
            options={
                'verbose_name': 'Інгредіент',
                'verbose_name_plural': 'Інгредіенти',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_categories', to='directory.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
