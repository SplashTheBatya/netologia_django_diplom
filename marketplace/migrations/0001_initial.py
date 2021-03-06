# Generated by Django 3.1.7 on 2021-04-08 11:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TimeField(choices=[('NEW', 'Новый'), ('IN_PROGRESS', 'В процессе'), ('DONE', 'Выполнен')], default='NEW')),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='marketplace.order')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='marketplace.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='position',
            field=models.ManyToManyField(related_name='position', through='marketplace.OrderProduct', to='marketplace.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.user'),
        ),
        migrations.CreateModel(
            name='Compilation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
                ('product', models.ManyToManyField(to='marketplace.Product')),
            ],
        ),
    ]
