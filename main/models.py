from django.db import models

from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=50 ,unique=True)
    slug = models.SlugField(max_length=50 ,primary_key=True)
    parent = models.ForeignKey('self', related_name='child', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stock = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.title



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.author_id}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)



