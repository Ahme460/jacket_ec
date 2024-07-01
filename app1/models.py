# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer_user(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        kwargs['using'] = kwargs.get('using', 'default')
        super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Products(models.Model):
    SALE_CHOICES = [
        ('sale', 'Sale'),
        ('sale_out', 'Sale Out'),
    ]

    size_select = [
        ('smile', 's'),
        ('medium', 'm'),
        ('large', 'l'),

    ]
    name = models.CharField(max_length=50)
    price = models.FloatField()
    about_product = models.TextField()
    photo = models.FileField()
    # count_order=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sale_status = models.CharField(max_length=10, choices=SALE_CHOICES, default='sale')
    # color=models.CharField(max_length=20,null=True)
    # size=models.CharField(max_length=50,null=True ,choices=size_select)
    details = models.TextField()

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if self.star > 5:
    #         self.star = 5
    #     return super().save(*args, **kwargs)


class SizesModel(models.Model):
    size_select = [
        ('smile', 's'),
        ('medium', 'm'),
        ('large', 'l'),

    ]
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="sizes")
    size = models.CharField(max_length=50, null=True, choices=size_select)


class ColorsModel(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="color")
    color = models.CharField(max_length=50, null=True)


class Orders(models.Model):
    order = models.TextField()
    customer = models.ForeignKey(Customer_user, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)  # تغيير هنا
    phone_user = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    location = models.TextField()

    def __str__(self):
        return self.customer.username


class CartModel(models.Model):
    customer = models.OneToOneField(Customer_user, on_delete=models.CASCADE, related_name="cart")

    @property
    def total_price(self):
        return sum([item.product.price * item.quantity for item in self.items.all()])


class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name="items", null=True)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} ({self.size}, {self.color})'
