from django.shortcuts import render , redirect
from . models import Customer
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from product_management.models import Product
from category_management.models import Category
from . import models
from django.core.paginator import Paginator

# Create your views here.

#home page
@never_cache 
def home(request):  
    items=Product.objects.filter(is_listed=True,category__is_listed=True)
    latst=Product.objects.order_by('-id')[:4]
    cont={'items':items,'latst':latst}
    
    return render(request,'index.html',cont)


#user login
@never_cache
def user_login(request):
    if "email" in request.session:
        return redirect("home")
    
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        try:
            user=Customer.objects.get(email=email,password=password)
        except:
            user=None
        
        if user is not None:
            if user.is_blocked:
                messages.error(request,'your account is blocked')
                return redirect('user_login')
            if user.is_verified:
                request.session['email']=email
                messages.success(request,'you are successfully logged in')
                return redirect('home')
            else:
                otp=models.generate_otp(user)
                models.otp_to_email(user,otp)
                return redirect('otp_verif',user.id)
        else:
            messages.error(request,'invalid email or password')

    return render(request,'login.html')

@never_cache
def register(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method=='POST':
        username=request.POST['f_name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        c_password=request.POST['c_password']
        join_date=timezone.now().date()
        

        if Customer.objects.filter(username=username).exists():
            messages.error(request,'username already exist')
            return render(request,'register.html')
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request,'email already exist')
            return render(request,'register.html')
        
        if Customer.objects.filter(phone=phone).exists():
            messages.error(request,'phone numbers already exits')
            return render(request,'register.html')
        
        if len(phone) != 10:
            messages.error(request,'phone number must be 10 digits')
            return render(request,'register.html')
        
        if password != c_password:
            messages.error(request,'passwords are not same')
            return render(request,'register.html')
        
        if len(password) < 6:
            messages.error(request,'password is not strong enough')
            return render(request,'register.html')
        
        # create instance and save it

        user=Customer(username=username,email=email,phone=phone,password=password,join_date=join_date)
        user.save()
        return redirect('otp_verif',id=user.id)

        # messages.success(request,'registeration is successfully finished , now you can login')
        # return redirect(user_login)

    return render(request,'register.html')


def user_logout(request):
    if 'email' in request.session:
        request.session.flush()
    messages.success(request,'you are successfully logged out')
    return redirect('user_login')


@never_cache
def otp_verif(request,id):
    
    if request.method=='POST':
        user=Customer.objects.get(id=id)
        e_otp=request.POST.get('otp')
        user_otp=user.otp_fld
        user_otp=int(user_otp)
        e_otp=int(e_otp)
        if e_otp==user_otp:
            user.is_verified=True
            user.save()
            messages.success(request,'OTP verification successfully finished now you can log in')
            return redirect('user_login')
        else:
            messages.error(request,'your OTP varification failed just try once more')
            return redirect('otp_verif',id)

    return render(request,'otp_verif.html')


def shop(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    item=Product.objects.filter(is_listed=True, category__is_listed=True)
    count=Product.objects.filter(is_listed=True, category__is_listed=True).count()
    product_paginator=Paginator(item,6)
    item=product_paginator.get_page(page)
    # if request.method ==  request.is_ajax():
    #     selected_option = request.POST.get('selected_option')
    # print(selected_option )
    contx={'item':item,'count':count}
    return render(request,'shop.html',contx)

def gallery(request):
    return render(request,'gallery.html')

def about_us(request):
    return render(request,'about_us.html')

def contact_us(request):
    return render(request,'contact_us.html')

@never_cache
def forget_pass(request):
    if request.method=='POST':
        femail=request.POST.get('fo_email')
        if Customer.objects.filter(email=femail).exists():
            user=Customer.objects.get(email=femail)
            id=user.id
            ot=models.generate_otp(user)
            models.otp_to_email(user,ot)
            return redirect('forget_otp',id)
        else:
            messages.error(request,'there is no account with this email, please create one !')
            return redirect('register')
            
    return render(request,'forget_pass.html')

def forget_otp(request,id):
    if request.method=='POST':
        e_otp=request.POST['otp']
        user=Customer.objects.get(id=id)
        user_otp=user.otp_fld
        if e_otp==user_otp:
            messages.success(request,'your otp verification successfully finished now you can reset password')
            return redirect('reset_pass',id)
        else:
            messages.error(request,'your OTP varification is failed')
            return redirect('forget_otp',id)

    return render(request,'otp_verif.html')

def reset_pass(request,id):
    if request.method=='POST':
        pass1=request.POST['re_password']
        pass2=request.POST['re_c_password']
        user=Customer.objects.get(id=id)
        if len(pass1) < 6:
            messages.error(request,'password is not strong enough')
            return redirect('reset_pass',id)
        if pass1==pass2:
            user.password=pass1
            user.save()
            messages.success(request,'your password successfully updated')
            return redirect('user_login')
        else:
            messages.error(request,'your password and confirm password are not same')
            return redirect('reset_pass',id)
    return render(request,'reset_pass.html')



