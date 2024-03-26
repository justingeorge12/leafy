from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bfr_login.models import Customer
from category_management.models import Category

# Create your views here.

#admin login
@never_cache
def admin_login(request):
    
    if request.user.is_authenticated:
        return redirect('admin_home')
    if request.method == 'POST':
        username=request.POST['ad_username']
        password=request.POST['ad_password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('admin_login')

    return render(request,'adminlogin.html')


#admin home


@never_cache 
@login_required(login_url='admin_login')
def admin_home(request):
    if 'email' in request.session:
        return render(request,'error.html')
    
    cate=Category.objects.all()

    name=User.objects.get(id=1)
    username = name.username if name else None
    cont={'cate':cate,'username':username}
    return render(request,'admin_home.html',cont)


#admin logout
@never_cache
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


#user management
@never_cache
@login_required(login_url='admin_login')
def user_manage(request):
    if 'email' in request.session:
        return render(request,'error.html')
    usr=Customer.objects.all().order_by('-id')
    cont={'usr':usr}
    return render(request,'user_manage.html',cont)

@never_cache
@login_required(login_url='admin_login')
def userblock(request,id):
    # if 'username' in request.session:
    blo=Customer.objects.get(id=id)
    blo.is_blocked=False
    blo.save()
    return redirect('user_manage')



# def block_user(request, id):
#     if "username" in request.session:
#         obj = CustomUser1.objects.get(id=id)
#         obj.is_blocked = True
#         obj.save()
#         return redirect("usermanage")





def userunblock(request,id):
    unbl=Customer.objects.get(id=id)
    unbl.is_blocked=True
    unbl.save()
    return redirect('user_manage')
