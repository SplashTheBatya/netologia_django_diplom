# Generated by Django 3.1.7 on 2021-04-19 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_auto_20210419_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product_id',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='marketplace.product'),
        ),
    ]
