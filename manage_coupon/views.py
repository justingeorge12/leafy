from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='admin_login')
def view_coupon(request):
    if 'email' in request.session:
        return render(request,'error.html')
    coupons=Coupons.objects.all().order_by('-id')
    contx={'coupons':coupons}
    return render(request,'coupon.html',contx)


@login_required(login_url='admin_login')
def create_coupon(request):
    if 'email' in request.session:
        return render(request,'error.html')
    if request.method == 'POST':
        title = request.POST.get('title')
        code = request.POST.get('code')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        quantity = request.POST.get('quantity')
        min_amount = request.POST.get('min_amount')
        discount_amount = request.POST.get('discount_amount')
        active_check = request.POST.get('active')
        active=True

        today = datetime.today().date()

        print(title,code,start_date,end_date,quantity,min_amount,discount_amount,active_check )
        print(active_check)

        if active_check == None:
            active=False

        if Coupons.objects.filter(title=title):
            messages.warning(request,'the title you are trying to add already in the list')
            return redirect('create_coupon')
        if title.strip() == '':
            messages.warning(request,'dont try to give a name only with space')
            return redirect('create_coupon')
        
        if Coupons.objects.filter(code=code):
            messages.warning(request,'the code you entered is already in the list')
            return redirect('create_coupon')
        if code.strip() == '':
            messages.warning(request,'dont try to give a code only with space')
            return redirect('create_coupon')

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start_date < today:
            messages.warning(request,'enter any day from today')
            return redirect('create_coupon')
        if end_date <= start_date:
            messages.warning(request,'enter a date after the starting date')
            return redirect('create_coupon')
        
        coupon=Coupons(
            title = title,
            code = code,
            discount_amount=discount_amount,
            start_date=start_date,
            end_date=end_date,
            quantity = quantity,
            min_amount = min_amount,
            active=active
        )
        coupon.save()
        messages.success(request,'coupon is added successfully')
            
    return render(request,'add_coupon.html')


@login_required(login_url='admin_login')
def inactive(request,id):
    act=Coupons.objects.get(id=id)
    act.active=False
    act.save()
    return redirect('view_coupon')


@login_required(login_url='admin_login')
def active(request,id):
    act=Coupons.objects.get(id=id)
    act.active=True
    act.save()
    return redirect('view_coupon')


@login_required(login_url='admin_login')
def edit_coupon(request,id):
    if 'email' in request.session:
        return render(request,'error.html')
    exst_details=Coupons.objects.get(id=id)
    contx={'exst_details':exst_details}
    # start_date=exst_details.start_date
    # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

    if request.method=='POST':
        title = request.POST.get('ed_title')
        code = request.POST.get('ed_code')
        start_date = request.POST.get('ed_start_date')
        end_date = request.POST.get('ed_end_date')
        quantity = request.POST.get('ed_quantity')
        min_amount = request.POST.get('ed_min_amount')
        discount_amount = request.POST.get('ed_discount_amount')
        active_check = request.POST.get('ed_active')
        active=True
        today = datetime.today().date()

        if active_check == None:
            active=False

        if title:
            if Coupons.objects.filter(title=title).exists():
                messages.warning(request,'the name is already in the list')
                return redirect('edit_coupon',id)
            elif title.strip() == '':
                messages.warning(request,"don't try to give only space ")
                return redirect('edit_coupon',id)
            else:
                exst_details.title=title
        if code:
            if Coupons.objects.filter(code=code).exists():
                messages.warning(request,'the code you entered is already in the list')
                return redirect('edit_coupon',id)
            elif code.strip() == '':
                messages.warning(request,"Don't try to give only space")
                return redirect('edit_coupon',id)
            else:
                exst_details.code=code
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if start_date < today:
                messages.warning(request,'Enter any day from today')
                return redirect('edit_coupon',id)
            else:
                exst_details.start_date=start_date

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date <= start_date:
                messages.warning(request,'enter a date after the starting date')
                return redirect('edit_coupon',id )
            else:
                exst_details.end_date=end_date
        if quantity:
            exst_details.quantity=quantity
        if min_amount:
            exst_details.min_amount=min_amount
        if discount_amount:
            exst_details.discount_amount=discount_amount
        

        exst_details.save()
        messages.success(request,'the field successfully edited')
        return redirect('view_coupon')

    return render(request,'edit_coupon.html',contx)