from django.shortcuts import render , redirect
from product_management . models import Product
from category_management . models import Category
from django.core.paginator import Paginator
from cart.models import Cart
from bfr_login.models import Customer
from django.contrib import messages
from .models import *
from django.views.decorators.cache import never_cache

# Create your views here.


def one_product(request,id):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        # check_cart=Cart.objects.filter(user_id=user)
    item=Product.objects.get(id=id) 
    contx={'item':item,}
    return render(request,'one_product.html',contx)
    


def drop_category(request,id): 
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    item=Product.objects.filter(category_id=id, is_listed=True, category__is_listed=True )
    count=Product.objects.filter(category_id=id).count()
    product_paginator=Paginator(item,6)
    item=product_paginator.get_page(page)
    con={'item':item,'count':count}
    return render(request,'drop_category.html',con)


def wishlist(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        if user.is_blocked:
            request.session.flush()
            messages.error(request,'you are blocked by admin')
            return redirect('user_login')

        wish_products=Wishlist.objects.filter(user_id=user).order_by('-id')
        contx={'products':wish_products}
        return render(request,'wishlist.html',contx)
    else:
        messages.error(request,'please login ..')
        return redirect('home')
    

@never_cache
def addtowish(request,id,frompage):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        product=Product.objects.get(id=id)
        print(frompage)
        if user.is_blocked:
            request.session.flush()
            messages.error(request,'you are blocked by admin')
            return redirect('user_login')
        if Wishlist.objects.filter(product_id=id,user_id=user).exists():
            messages.error(request,'the product already in the wishlist')
            if frompage =='one_product':
                return redirect('one_product',id)
            elif frompage == 'home':
                return redirect('home')
            else:
                return redirect('shop')
            
        else:
            wishlist=Wishlist(
                user_id=user,
                product_id=product
            )
            wishlist.save()
            if frompage== 'one_product':
                return redirect('one_product',id)
            if frompage== 'shop' :
                return redirect('shop')
            if frompage == 'home':
                return redirect('home')
    else:
        messages.error(request,'please login and try againn..')
        if frompage=='one_product':
            return redirect('one_product',id)
        elif frompage == 'shop':
            return redirect('shop')
        else:
            return redirect('home')
    

@never_cache
def deletewish(request,id):
    print(id)
    itemto_remo=Wishlist.objects.get(id=id)
    if itemto_remo:
        itemto_remo.delete()
    return redirect('wishlist')

def movetocart(request,id):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        print(user)

        wish=Wishlist.objects.get(id=id)
        product_id=wish.product_id
        print(product_id)
        print(product_id.price)

        if Cart.objects.filter(user_id=user,product_id=product_id).exists():
            messages.error(request,'this product already in your cart')
            return redirect('wishlist')
        else:
            addtowish=Cart(
                user_id=user,
                product_id=product_id,
                quantity=1,
                total=product_id.price 
            )
            addtowish.save()
            wish.delete()
            return redirect('wishlist')


        

    
    # product_id=Product.objects.get(id=id)
    return redirect('wishlist')