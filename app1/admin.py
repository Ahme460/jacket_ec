from django.contrib import admin
from .models import *

models = [Customer_user, Products, SizesModel, ColorsModel, CartItem, Orders, CartModel]

for i in models:
    admin.site.register(i)

# Register your models here.
# admin.site.register(Customer_user)