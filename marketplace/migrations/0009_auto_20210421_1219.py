# Generated by Django 3.1.7 on 2021-04-21 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_auto_20210419_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='summary',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
