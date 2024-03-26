from django.db import models
from bfr_login.models import Customer

# Create your models here.


class Address(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    address=models.TextField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    number=models.BigIntegerField()
    pincode=models.BigIntegerField()
    is_available=models.BooleanField(default=True,null=True)

    def __str__(self) -> str:
        return f"'{self.name}'s address"


   
class Wallet_User(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(max_length=50)        #credit debit
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)