from django.db import models
from bfr_login.models import Customer
from product_management.models import Product

# Create your models here. 


class Wishlist(models.Model):
    user_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user_id}'s Wishlist"