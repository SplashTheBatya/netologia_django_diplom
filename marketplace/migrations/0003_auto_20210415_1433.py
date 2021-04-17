# Generated by Django 3.1.7 on 2021-04-15 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_auto_20210415_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый'), ('IN_PROGRESS', 'В процессе'), ('DONE', 'Выполнен')], default='NEW', max_length=255),
        ),
    ]
