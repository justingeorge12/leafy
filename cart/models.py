from django.db import models
from bfr_login.models import Customer
from product_management.models import Product
from manage_coupon.models import Coupons

# Create your models here.

class Cart(models.Model):
    user_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total=models.IntegerField(blank=True, null=True)
    category=models.CharField(max_length=50)
    # size=models.ForeignKey(varient,on_delete=models.CASCADE,null=True)
    product_price=models.IntegerField(blank=True,null=True)
    coupon_active = models.BooleanField(default= False , null=True)

    def __str__(self) -> str:
        return f"{self.product_id.name} - {self.quantity}"
    
    def subtotal(self):
        return self.product_id.price * self.quantity
    

class Checkout(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sub_total = models.IntegerField(null=True)
    coupon = models.ForeignKey(Coupons, on_delete= models.SET_NULL, null=True)
    coupon_active = models.BooleanField(default= False , null=True)

