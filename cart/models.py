from django.db import models

from account.models import User
from main.models import Product


class Cart(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, blank=True, null=True, default=False)
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE, blank=True, null=True)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.count}"


class CartProduct(models.Model):
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

