from django.db import models
from bfr_login.models import Customer
from userprofile.models import Address
from product_management.models import Product
from django.utils import timezone

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.CharField(max_length=10)
    order_date = models.DateField(auto_now_add=True)
    payment_mode=models.CharField(max_length=15,default='COD')
    

    def __str__(self) -> str:
        return f"{self.user}'s Order {self.id}"
    


class Ordered_items(models.Model):
    # STATUS_CHOICES = (
    #     ( 'Order confirmed', 'Order confirmed' ),
    #     ( 'Shipped', 'Shipped' ),
    #     ( 'Out for delivery', 'Out for delivery' ),
    #     ( 'Delivered', 'Delivered' ),
    #     ( 'Cancelled', 'Cancelled' ),
    # )
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    addr = models.ForeignKey(Address,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    total_amount = models.IntegerField()              #decimal field , subtotal
    category = models.CharField(max_length=50)
    user = models.IntegerField()                      # foreignkey field
    expected_date = models.DateField(null=True)


class CancelledOrder(models.Model):
    order_id = models.ForeignKey(Ordered_items,on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    cancel_reason = models.TextField(null=True, blank=True)
    cancel_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelled order item: {self.order_id.product} in order {self.order_id.order_id}"
    


class OrderReturns(models.Model):
    order_id = models.ForeignKey(Ordered_items, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    request_date = models.DateField(auto_now_add=True, null=True)
    pickup_date = models.DateField(null=True, blank=True)
