from django.shortcuts import render , redirect
from .models import Category
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

#category list
@login_required(login_url='admin_login')
def category(request):
    if 'email' in request.session:
        return render(request,'error.html')
    if request.user.is_authenticated:  
        cate=Category.objects.all()
        context={'cate':cate}
    return render(request,'category.html',context)

# add category
@login_required(login_url='admin_login')
def add_category(request):
    if 'email' in request.session:
        return render(request,'error.html')
    if request.method=='POST':
        add_cat=request.POST['add_cat']
        ob=Category.objects.filter(name=add_cat).exists()
        if not ob:
            obj=Category(name=add_cat)
            obj.save()
            messages.success(request,'your category successfully added')
            return redirect('category')
        else:
            messages.error(request,'the category you trying to add is already there in category')
            return redirect('category')

    return render(request,'add_category.html')

#edit category
@login_required(login_url='admin_login')
def edit_category(request,id):
    catt=Category.objects.get(id=id)
    print(catt.name )
    if request.method=='POST':
        edit_cat=request.POST['edit_cat']
        if Category.objects.filter(Q(name=edit_cat) & ~Q(id=id)):
            messages.error(request,'the name you are trying to create is already there in category list')
            return redirect('edit_category',id)
        else:           
            catt.name=edit_cat
            catt.save()
            return redirect('category')
        
    return render(request,'edit_category.html',{'catt':catt})


# list category
@login_required(login_url='admin_login')
def list_cate(request,id):
    obj=Category.objects.get(id=id)
    obj.is_listed=True
    obj.save()
    return redirect('category')

# unlist category
@login_required(login_url='admin_login')
def unlist_cate(request,id):
    obj=Category.objects.get(id=id)
    obj.is_listed=False
    obj.save()
    return redirect('category')