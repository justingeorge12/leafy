from django.shortcuts import render,redirect
from bfr_login.models import Customer
from django.contrib import messages
from .models import *
from manage_order.models import *
from django.views.decorators.cache import never_cache
from product_management.models import Product
from django.utils import timezone
from datetime import timedelta

# Create your views here.


def user_profile(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        cstmr=Customer.objects.get(id=user.id)

        adda=Address.objects.filter(user=user.id,is_available=True)

        ordrr=Order.objects.filter(user=user.id).order_by('-id')

        wall=Wallet_User.objects.filter(user_id=user.id)
        wall_baln=Wallet_User.objects.filter(user_id=user.id).order_by('-id').first()
        
        cont={'cstmr':cstmr,'adda':adda,'ordrr':ordrr,'wall':wall,'wall_baln':wall_baln}
    return render(request,'profile.html',cont)

def change_pass(request):
    if request.method=='POST':
        if 'email' in request.session:
            email=request.session.get('email')
            user=Customer.objects.get(email=email)
            cstmr=Customer.objects.get(id=user.id)
            curr_pass=request.POST['curr_pass']
            new_pass=request.POST['new_pass']
            conf_pass=request.POST['conf_pass']
            if curr_pass == cstmr.password:
                if len(new_pass)>6:
                    if new_pass == conf_pass:
                        cstmr.password=new_pass
                        cstmr.save()
                    else:
                        messages.error(request,'entered passwords are not same')
                        return redirect('change_pass')
                else:
                    messages.error(request,'please enter atleast six letters')
                    return redirect('change_pass')
                
            else:
                messages.error(request,'entered password is not your password')
                return redirect('change_pass')
        else:
            return redirect('user_login')
                
    return redirect('user_profile')

def add_address(request):
    if request.method=='POST':
        if 'email' in request.session:
            email=request.session.get('email')
            user=Customer.objects.get(email=email)
            cstmr=Customer.objects.get(id=user.id)
            name=request.POST['full_name']
            addr=request.POST['address']
            city=request.POST['city']
            state=request.POST['state']
            country=request.POST['country']
            number=request.POST['phone']
            pincode=request.POST['postcode']
            if len(pincode) == 6:
                if len(number) == 10:
                    add=Address(user=cstmr,
                                name=name,
                                address=addr,
                                city=city,
                                state=state,
                                country=country,
                                number=number,
                                pincode=pincode,
                                )
                    add.save()
                    messages.success(request,'address added successfully')
                else:
                    messages.error(request,'phone number must be 10 digits')
                    return redirect('add_address')
            else:
                messages.error(request,'pincode must be 6 digits')
                return redirect('add_address')
        else:
            return redirect('user_login')
    return redirect('user_profile')


def delete_add(request,id):
    add=Address.objects.get(id=id)
    add.is_available=False
    add.save()
    return redirect('user_profile')


def edit_pro(request,id):
    user=Customer.objects.get(id=id)
    contx={'user':user}
    if request.method=='POST':
        username=request.POST['edit_username']
        phone=request.POST['edit_num']
        if username:
            user.username=username
        if phone:
            if len(phone)==10:
                user.phone=phone
            else:
                messages.error(request,'phone number must be 10 digits')
        user.save()
        messages.success(request,'your details has successfully edited')
        return redirect('user_profile')
    return render(request,'edit_pro.html',contx)



def edit_add(request,id):
    add=Address.objects.get(id=id)
    contx={'add':add}
    if request.method=='POST':
        name=request.POST['edit_name']
        addr=request.POST['edit_address']
        city=request.POST['edit_city']
        state=request.POST['edit_state']
        country=request.POST['edit_country']
        number=request.POST['edit_phone']
        pincode=request.POST['edit_postcode']

        
        if name:
            add.name=name
        if addr:
            add.address=addr
        if city:
            add.city=city
        if state:
            add.state=state
        if country:
            add.country=country
        if number:
            if len(number)==10:
                add.number=number
            else:
                messages.error(request,'phone number should be 10 digits')
                
        if pincode:
            if len(pincode) == 6:
                add.pincode=pincode
            else:
                messages.error(request,'pincode should be 6 digits')
        add.save()
        messages.success(request,'your new details successfull edited')
        return redirect('user_profile')
        

    return render(request,'edit_add.html',contx)


def order_detail(request,id):

    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        # ordr_addr=Order.objects.filter(user=user.id )
        order_items=Ordered_items.objects.filter(user=user.id,order_id=id)
        print(order_items)
        contxx={'order_items':order_items}
    return render(request,'order_detail.html',contxx)

@never_cache
def cancel_order(request,id):
    if 'email' in request.session:
        email=request.session.get('email')
    user=Customer.objects.get(email=email)
    cstmr=Customer.objects.get(id=user.id)
    date=timezone.now().date()

    cancl=Ordered_items.objects.get(id=id)

    cancl_database=CancelledOrder(
        order_id = cancl,
        user_id = cstmr,
        cancel_date = date
    )
    cancl_database.save()

    quantity_ordered=cancl.quantity
    cancl.status='cancelled'
    cancl.save()

    prod=Product.objects.get(id=cancl.product_name.id)
    prod.quantity=prod.quantity+quantity_ordered
    prod.save()
    
    
    paymnt_mode_used=cancl.order_id.payment_mode
    try:
        user_wallt=Wallet_User.objects.filter(user_id=cstmr).order_by('-id').first()
    
        if not user_wallt:
            balancee=0
        else:
            balancee=user_wallt.balance
        if paymnt_mode_used != 'COD':
            
            wallet = Wallet_User(
                user_id=user,
                transaction_type='credit',
                amount=cancl.total_amount,
                balance=balancee+cancl.total_amount
                
            )
            wallet.save()
    except Exception as e:
        print(e,'excepttttttttioooooonn')


    return redirect(order_detail,id)

@never_cache
def return_order(request,id):
    if 'email' in request.session:
        email=request.session.get('email')
    user=Customer.objects.get(email=email)
    cstmr=Customer.objects.get(id=user.id)
    date=timezone.now().date()

    retrn_pro=Ordered_items.objects.get(id=id)

    retrn_database=OrderReturns(
        order_id = retrn_pro,
        user = cstmr,
        request_date = date,
        pickup_date = date + timedelta(days=8),

    )
    retrn_database.save()

    retrn_pro.status = 'returned'
    retrn_pro.save()

    quantity_ordered=retrn_pro.quantity
    prod=Product.objects.get(id=retrn_pro.product_name.id)
    prod.quantity=prod.quantity+quantity_ordered
    prod.save()

    try:
        user_wallt=Wallet_User.objects.filter(user_id=cstmr).order_by('-id').first()

        if not user_wallt:
            balancee=0
        else:
            balancee=user_wallt.balance
        wallet=Wallet_User(
            user_id=user,
            transaction_type='credit',
            amount=retrn_pro.total_amount,
            balance=balancee+retrn_pro.total_amount
        )
        wallet.save()
    except Exception as e:
        print(e,'exxxptn')


    return redirect(order_detail,id)
    
