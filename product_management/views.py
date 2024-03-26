from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from category_management.models import Category
from .models import Product
from django.contrib import messages
from django.db.models import Q 
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url='admin_login')
def product(request):
    if 'email' in request.session:
        return render(request,'error.html')
    # page=1
    # if request.GET:
    #     page=request.GET.get('page',1)
    prod=Product.objects.all().order_by('-id')
    # product_paginator=Paginator('page',6)
    # prod=product_paginator.get_page(page)
    cont={'pro':prod}
    return render(request,'product.html',cont)

@login_required(login_url='admin_login')
def add_product(request):
    if 'email' in request.session:
        return render(request,'error.html')
    
    cat=Category.objects.all()

    if request.method=='POST':
        pd_name=request.POST['pd_name']
        category=request.POST['category']
        slt_cat=Category.objects.get(id=category)
        price=request.POST['price']
        og_price=request.POST['og_price']
        color=request.POST['color']
        vendor=request.POST['vendor']
        quantity=int(request.POST['quantity'])
        description=request.POST['description']
        
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3', None)
        image4 = request.FILES.get('image4', None)

        
        if Product.objects.filter(name=pd_name).exists():
            messages.error(request,'the product name already there in list')
            return redirect(add_product)
        else:
            if int(price) and int(og_price) and quantity >0:
                obj=Product(name=pd_name,
                            category=slt_cat,
                            price=price,
                            og_price=og_price,
                            quantity=quantity,
                            color=color,
                            vendor=vendor,
                            description=description,
                            image1=image1,
                            image2=image2,
                            image3=image3,
                            image4=image4)
                obj.save()
                return redirect('product')
            else:
                messages.error(request,'entered price or quantity is not valid')
                return redirect("add_product")
    return render(request,'add_product.html',{'cat':cat})

@login_required(login_url='admin_login')
def edit_product(request,id):
    cat=Category.objects.all()
    pro=Product.objects.get(id=id)

    contx={'cat':cat,
           'pro':pro}

    if request.method=='POST':
        pd_name=request.POST['ed_name']
        category=request.POST['ed_product']
        slt_cat=Category.objects.get(id=category)
        price=request.POST['ed_price']
        og_price=request.POST['ed_og_price']
        color=request.POST['ed_color']
        vendor=request.POST['ed_vendor']
        quantity=int(request.POST['ed_quantity'])
        description=request.POST['ed_descri']
        image1=request.FILES.get('ed_image1',None)
        image2=request.FILES.get('ed_image2',None)
        image3=request.FILES.get('ed_image3',None)
        image4=request.FILES.get('ed_image4',None)


        if Product.objects.filter(Q(name=pd_name) & ~Q(id=id)).exists():
            messages.error(request,'the name you are trying to add is already there in the list')
            return redirect('edit_product',id)
        else:
            if pd_name:
                pro.name=pd_name
            if slt_cat:
                pro.category=slt_cat
            if price:
                if int(price) > 0:
                    pro.price=price
                else:
                    messages.error(request,'entered price is not valid')
            if og_price:
                if int(price) > 0:
                    pro.og_price=og_price
                else:
                    messages.error(request,'entered price is not valid')
            if color:
                pro.color=color
            if vendor:
                pro.vendor=vendor
            if quantity:
                if quantity >= 0:
                    pro.quantity=quantity
                else:
                    messages.error(request,'please enter valid number')
            if description:
                pro.description=description
            if image1:
                pro.image1=image1
            if image2:
                pro.image2=image2
            if image3:
                pro.image3=image3
            if image4:
                pro.image4=image4
            pro.save()
            return redirect('product')
    return render(request,'edit_product.html',contx )



def edit_varint(request):
    return render(request,'edit_varint.html')



@login_required(login_url='admin_login')
def unlist_pro(request,id):
    obj=Product.objects.get(id=id)
    obj.is_listed=False
    obj.save()
    return redirect('product')


@login_required(login_url='admin_login')
def list_pro(request,id):
    obj=Product.objects.get(id=id)
    obj.is_listed=True
    obj.save()
    return redirect('product')