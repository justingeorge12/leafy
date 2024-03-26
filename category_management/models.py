from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    is_listed=models.BooleanField(default=True)

    def __str__(self):
        return self.name
