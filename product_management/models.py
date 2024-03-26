from django.db import models
from category_management.models import Category

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.IntegerField()
    description=models.TextField()
    quantity=models.IntegerField()

    image1=models.ImageField(upload_to='image/',blank=True)
    image2=models.ImageField(upload_to='image/', blank=True)
    image3=models.ImageField(upload_to='image/', blank=True)
    image4=models.ImageField(upload_to='image/', blank=True)
    is_listed=models.BooleanField(default=True)
    og_price=models.IntegerField(null=0)
    vendor=models.CharField(max_length=30,default='leafy')
    color=models.CharField(max_length=20,default='green')



class variant(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.CharField(max_length=4)
    quantity=models.IntegerField()

                

