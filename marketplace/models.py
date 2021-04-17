from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models import CASCADE


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.TimeField(
        auto_now_add=True
    )
    updated_at = models.TimeField(
        auto_now=True
    )


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    product_id = models.ForeignKey(Product, on_delete=CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    created_at = models.TimeField(
        auto_now_add=True
    )
    updated_at = models.TimeField(
        auto_now=True
    )


class OrderStatusChoices(models.TextChoices):
    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN_PROGRESS", "В процессе"
    DONE = "DONE", "Выполнен"


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    position = models.ManyToManyField(Product, through='OrderProduct', related_name='position')
    status = models.CharField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
        max_length=255
    )
    created_at = models.TimeField(
        auto_now_add=True
    )
    updated_at = models.TimeField(
        auto_now=True
    )
    summary = models.PositiveIntegerField()


class OrderProduct(models.Model):
    Order = models.ForeignKey(
        Order,
        on_delete=CASCADE,
        related_name='order'
    )
    Product = models.ForeignKey(
        Product,
        on_delete=CASCADE,
        related_name='product'
    )
    amount = models.PositiveIntegerField()


class Compilation(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ManyToManyField(Product)
    created_at = models.TimeField(
        auto_now_add=True
    )
    updated_at = models.TimeField(
        auto_now=True
    )
