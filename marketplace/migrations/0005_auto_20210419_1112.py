# Generated by Django 3.1.7 on 2021-04-19 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_order_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=510),
        ),
    ]
