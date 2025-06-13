from django.db import models
from uuid import uuid4

from products.models import Product

from datetime import datetime


class Order(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

class Cart(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    products = models.ManyToManyField(Order, 'products')