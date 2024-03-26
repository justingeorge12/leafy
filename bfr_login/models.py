from django.db import models
import random
from django.core.mail import send_mail
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Customer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password=models.CharField(max_length=100)
    join_date = models.DateField()
    phone = models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    is_blocked=models.BooleanField(default=False)
    otp_secret=models.CharField(max_length=100)
    otp_fld=models.CharField(max_length=4)
    # referral_link=models.CharField(max_length=255,unique=True)
    

    def __str__(self):
        return self.username
    



# generate otp
def generate_otp(instance):
    # length=4
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    instance.otp_fld = otp  # Update the OTP field of the current instance
    instance.save()
    return otp 

#send OTP email
def otp_to_email(instance,otp):
    subject='OTP Verification'
    message = f"your OTP varifiation is : {otp}"
    from_email= 'plantlyjustin@gmail.com'
    send_mail(subject,message,from_email,[instance.email])


@receiver(post_save, sender=Customer)
def generate_and_send_otp(sender,instance,created,**kwargs):
    if created:
        otp=generate_otp(instance)
        otp_to_email(instance,otp)
    
