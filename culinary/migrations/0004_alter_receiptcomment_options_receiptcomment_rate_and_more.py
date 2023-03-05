# Generated by Django 4.1.7 on 2023-03-04 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('culinary', '0003_alter_receipt_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receiptcomment',
            options={'ordering': ['-created_at'], 'verbose_name': 'Оцінка рецепту', 'verbose_name_plural': 'Оцінки рецепту'},
        ),
        migrations.AddField(
            model_name='receiptcomment',
            name='rate',
            field=models.IntegerField(choices=[(1, 'very bad'), (2, 'bad'), (3, 'normal'), (4, 'good'), (5, 'perfect')], default=5),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='culinary.receipt'),
        ),
        migrations.AlterField(
            model_name='receiptcomment',
            name='text',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.DeleteModel(
            name='ReceiptVote',
        ),
    ]