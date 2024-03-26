from django.shortcuts import render , redirect
from django.http import HttpResponse
from bfr_login.models import Customer
from django.contrib import messages
from .models import Cart
from product_management.models import Product
from django.db.models import Sum
from django.http import JsonResponse
from userprofile.models import *
from manage_order.models import Order
from manage_order.models import Ordered_items
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import never_cache
from manage_order.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseBadRequest
from manage_coupon.models import *
from datetime import datetime

import razorpay
from .models import Checkout




# Create your views here.


def addtocart(request,id):
    if request.method =='POST':
        qntty = int(request.POST.get('qantity'))
        produ = Product.objects.get(id=id)

    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        custm=Customer.objects.get(id=user.id)
        # print(custm)
        if user.is_blocked:
            request.session.flush()
            messages.error(request,'you are blocked by admin')
            return redirect('user_login')
        else:
            obj,created= Cart.objects.get_or_create(user_id=custm,
                    product_id=produ
                    )
            
            if created:
                if obj.quantity+qntty<produ.quantity:
                    obj.quantity=qntty
                    obj.total=produ.price*qntty
                    obj.save()
                else:
                    messages.error(request,f"there are only {produ.quantity} stocks available")


                # print(produ.price)
                
            else:
                if obj.quantity+qntty<=produ.quantity:
                    if obj.quantity+qntty <=6:
                        obj.quantity=obj.quantity+qntty
                        obj.total=obj.total+produ.price*qntty
                        print(produ.price)
                        obj.save()  
                    else:
                        messages.error(request,'maximum quantity that you can add is 5')
                        return redirect('one_product',id)
                else:
                    messages.error(request,f"there are only {produ.quantity} stocks available")
    else:
        messages.error(request,'please login..')
        return redirect('one_product',id )
    # return redirect('one_product',id )

    return redirect('one_product',id )


def showcart(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        # custm=Customer.objects.get(id=user.id)
        # print(user)
        if user.is_blocked:
            request.session.flush()
            messages.error(request,'you are blocked by admin')
            return redirect('user_login')
        else:
            items=Cart.objects.filter(user_id=user).order_by('-id')
            # amount=Cart.objects.aggregate(Sum('total'))
            # amount=amount['total__sum']
            amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
            cnt=Cart.objects.filter(user_id=user).count()
            cont={'items':items,'amount':amount,'cnt':cnt,'user':user}

    return render(request,'cart.html',cont)



def update_quant(request):
    if request.method == 'POST':
        product_id = int(request.POST.get("products_id"))
        pro_id=Cart.objects.get(id=product_id)
        action=request.POST.get("action")
        item = Cart.objects.get(id=product_id)

        if action == "plus":
            if item.quantity < 6:
                if item.quantity < pro_id.product_id.quantity:
                    item.quantity = item.quantity + 1
                    item.total=item.total+pro_id.product_id.price
            #     else:
            #         messages.error(request,'item is not more available')
            # else:
            #     messages.error(request,'you can order only 6 product at a time')
            
        else:
            if item.quantity > 0:
                item.quantity = item.quantity - 1
                item.total=item.total-pro_id.product_id.price
        item.save()

        return JsonResponse({"status":"successfully updated"})
    


#delete product from cart
def remove(request,id):
    rem=Cart.objects.get(id=id)
    if rem:
        rem.delete()
    return redirect('showcart')



# @never_cache
# def checkout(request,id):
#     if 'email' in request.session:
#         email=request.session.get('email')
#         user=Customer.objects.get(email=email)
#         addr=Address.objects.filter(user=id,is_available=True)
#         email=request.session.get('email')
#         user=Customer.objects.get(email=email)
#         items=Cart.objects.filter(user_id=user)
#         amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
#         date=timezone.now().date()
#         cnt=Cart.objects.filter(user_id=user).count()
        
#         cont={'addr':addr,'items':items,'amount':amount,'cnt':cnt}

#         # if not items:
#         #     return redirect('showcart')
        
#         if request.method == 'POST':
#             sel_addr=request.POST.get('selected_address',None)
#             addrss=Address.objects.get(id=sel_addr)
#             if addrss is None:
#                 messages.error(request,'there is no address please add one ')
#                 return redirect('checkout')
            
            

#             if items:
#                 obj=Order(
#                     user=user,
#                     address=addrss,
#                     total_amount=amount,
#                     order_date=date
#                 )
#                 obj.save()


#                 for i in items:
#                     order_item=Ordered_items(
#                         order_id = obj,
#                         product_name = i.product_id,
#                         user = obj.user.id,
#                         addr = addrss,
#                         quantity = i.quantity,
#                         status = 'ordered',
#                         # category = i.category,
#                         total_amount = i.total,
#                         expected_date = date + timedelta(days=7)     
#                     )
                
#                     order_item.save()

#                     # decres_qnty=Product.objects.get(id=i.product_id.id)
#                     # decres_qnty.quantity=  decres_qnty.quantity-order_item.quantity
#                     # decres_qnty.save()
                    
                    

                    
#                 items.delete()
            
               
            

#             order_detail=Order.objects.get(id=obj.id)
#             exp_day=order_detail.order_date + timedelta(days=8)
#             final_amount=order_item.total_amount
            

        
#             contx={'order_detail':order_detail,
#                    'exp_day':exp_day,
#                    }


#             return render(request,'success_oder.html',contx)
        
        
#     return render(request,'checkout.html',cont)








def add_addrs(request):
    if request.method=='POST':
        if 'email' in request.session:
        
            email=request.session.get('email')
            user=Customer.objects.get(email=email)
            name=request.POST['full_name']
            addr=request.POST['address']
            city=request.POST['city']
            state=request.POST['state']
            country=request.POST['country']
            number=request.POST['phone']
            pincode=request.POST['postcode']
            
            # if name.strip():
            #     if len(name)>2:
            #         print('something is there')
                
            # else:
            #     print('i dont know what is happening ')
            
            if len(pincode) == 6:
                if len(number) == 10:
                    new_add=Address(
                        user=user,
                        name=name,
                        address=addr,
                        city=city,
                        state=state,
                        country=country,
                        number=number,
                        pincode=pincode,
                    )
                    new_add.save()
                    messages.success(request,'address added successfully')
                    return redirect('checkout',user.id)
                else:
                    messages.error(request,'phone number should be 10 digits')
            else:
                messages.error(request,'postcode should be 6 digit')
        else:
            return redirect('user_login')
        
    return render(request,'add_addrss.html')



  
        



# @never_cache             # check out the working one moved to placeorder 
# def checkout(request,id):
#     if 'email' in request.session:
#         email=request.session.get('email')
#         user=Customer.objects.get(email=email)
#         addr=Address.objects.filter(user=id,is_available=True)
#         items=Cart.objects.filter(user_id=user)
#         amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
#         date=timezone.now().date()
#         cnt=Cart.objects.filter(user_id=user).count()
        
#         cont={'addr':addr,'items':items,'amount':amount,'cnt':cnt}

        
#         checkout_obj,created=Checkout.objects.get_or_create(
#             user_id=user.id,
#             sub_total= amount
#         )
#         final_amount=checkout_obj.sub_total


#         return render(request,'checkout.html',cont) 
        
        
#     return render(request,'checkout.html',cont)



# # for cash on delivery COD
# @never_cache
# def cod(request):               #working one
#     if 'email' in request.session:
#         email=request.session.get('email')
#         user=Customer.objects.get(email=email)
#         amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
#         cart_obj=Cart.objects.filter(user_id=user)
#         date=timezone.now().date()

#         if request.method =='POST':
#             sel_addr=request.POST.get('selected_address')
#             addrss=Address.objects.get(id=sel_addr)
            
#             payment_method = request.POST.get('payment_option')
            
#             if payment_method == 'cod':            
#                 if cart_obj:
#                     obj=Order(
#                         user=user,
#                         address=addrss,
#                         total_amount=amount,
#                         order_date=date,
#                         payment_mode=payment_method

#                     )
#                     obj.save()

#                     for i in cart_obj:
#                         order_item=Ordered_items(
#                             order_id = obj,
#                             product_name = i.product_id,
#                             user = obj.user.id,
#                             addr = addrss,
#                             quantity = i.quantity,
#                             status = 'ordered',
#                             # category = i.category,
#                             total_amount = i.total,
#                             expected_date = date + timedelta(days=8)

#                         )
#                         order_item.save()
#                         # decres_qnty=Product.objects.get(id=i.product_id.id)
#                         # decres_qnty.quantity=  decres_qnty.quantity-order_item.quantity
#                         # decres_qnty.save()
                        
#                     cart_obj.delete()

#                 return redirect('success',obj.id)
               
#     return redirect('user_login' )








def success(request,id):          #working
    order_detail=Order.objects.get(id=id)
    print(id)
    exp_day=order_detail.order_date+timedelta(days=8)
    # addrss=Order.objects.get(id=id)
    # final_amount=order_detail.total_amount
    contx={'order_detail':order_detail,
           'exp_day':exp_day}
    return render(request,'success_oder.html',contx)



razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# @never_cache
# def checkout(request,id):        #old one deletee it
#     if 'email' in request.session:
#         email=request.session.get('email')
#         user=Customer.objects.get(email=email)
#         addr=Address.objects.filter(user=id,is_available=True)
#         items=Cart.objects.filter(user_id=user)
#         amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
#         date=timezone.now().date()
#         cnt=Cart.objects.filter(user_id=user).count()
        
#         cont={'addr':addr,'items':items,'amount':amount,'cnt':cnt}
        
#         checkout_obj,created=Checkout.objects.get_or_create(
#             user_id=user.id,
#             sub_total= amount
#         )
#         final_amount=checkout_obj.sub_total

#         return render(request,'checkout.html',cont)  
#     return render(request,'checkout.html',cont)




# for razor pay
def placeorder(request,id):      
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        # addr=Address.objects.filter(user=id,is_available=True)
        items=Cart.objects.filter(user_id=user)
        t_amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
        date=timezone.now().date()
        cnt=Cart.objects.filter(user_id=user).count()
        coupons=Coupons.objects.filter(active=True,start_date__lte=date, end_date__gte=date) # 
        
        # cont={'addr':addr,'items':items,'amount':t_amount,'cnt':cnt}

        abbb=sel_adresss=request.POST.get('selected_user_id')
        print(abbb,'bbbbbbbbbbbbbbbbbbbbbbbbbb')
         


        currency = 'INR'
        amount = t_amount 

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                currency=currency,
                                                payment_capture='0'))
        
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/paymenthandler/'

            # we need to pass these details to frontend.
        # context = {}
        # context['razorpay_order_id'] = razorpay_order_id
        # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        # context['razorpay_amount'] = amount
        # context['currency'] = currency
        # context['callback_url'] = callback_url
        # context['addr'] = addr
        # context['items'] = items
        # context['amount'] = t_amount
        # context['cnt'] = cnt

        contxx={'razorpay_order_id':razorpay_order_id,
                'razorpay_merchant_key':settings.RAZOR_KEY_ID,
                'razorpay_amount':amount,
                'currency':currency,
                'callback_url':callback_url,
                # 'addr':addr,
                'items':items,
                'amount':t_amount,
                'cnt':cnt,
                'coupon':coupons
                }
        

        return render(request, 'checkout.html', contxx)
    else:
        return redirect('user_login')





# def checkk(request):
#     if request.method == 'POST':
#         method = request.POST.get('payment_option')
#         print(method)
#         print('asdlfjksdlfjksdlfjksdfjk')
#         print('__________!!!!!!!!!!_____________')
#     return redirect('paymenthandler')





@csrf_exempt
def paymenthandler(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        t_amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']
        cart_obj=Cart.objects.filter(user_id=user)
        date=timezone.now().date()
        
        a=sel_adresss=request.POST.get('selected_user_id')
        selected_user_id = request.POST.get('selected_user_id')
        print(a)
        print(selected_user_id)
        a=request.POST.get('selected_address')
        print(a,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print('address id == ' , a)
        paymentoption=request.POST.get('paymentoption')
        print(paymentoption)
        print(paymentoption,'--------------_______________-------------_________')

        

        

        # only accept POST request.
        if request.method == 'POST':
            method = request.POST.get('payment_option')
            print(method)

            if method == 'cod':
                if cart_obj:
                    obj=Order(
                        user=user,
                        total_amount=t_amount,
                        order_date=date,
                        payment_mode='cod'
                    )
                    obj.save()
                    for i in cart_obj:
                        order_item=Ordered_items(
                            order_id = obj,
                            product_name=i.product_id,
                            user = obj.user.id,
                            quantity = i.quantity,
                            status = 'ordered',
                            total_amount = i.total,
                            expected_date = date + timedelta(days=8),
                            addr_id='2',
                        )
                        order_item.save()
                        decres_qnty=Product.objects.get(id=i.product_id.id)
                        decres_qnty.quantity=  decres_qnty.quantity-order_item.quantity
                        decres_qnty.save()
                    cart_obj.delete()

                return redirect('success',obj.id)
            

            # walllet payment  
            if method == 'wallet':
                try:
                    wallet_user = Wallet_User.objects.filter(user_id=user).order_by("-id").first()

                    if t_amount > int(wallet_user.balance):
                        messages.error(request,'you have not enough money to order')
                        return redirect('showcart')
                    if cart_obj:
                        obj=Order(
                            user=user,
                            total_amount=t_amount,
                            order_date=date,
                            payment_mode='wallet'
                        )
                        obj.save()
                        for i in cart_obj:
                            order_item=Ordered_items(
                                order_id = obj,
                                product_name=i.product_id,
                                user = obj.user.id,
                                quantity = i.quantity,
                                status = 'ordered',
                                total_amount = i.total,
                                expected_date = date + timedelta(days=8),
                                addr_id='2',
                            )
                            order_item.save()

                            # wallt_decres = Wallet_User.objects.get(user_id=user)
                            # print(wallt_decres)
                            # print(wallt_decres.balance)

                            decres_qnty=Product.objects.get(id=i.product_id.id)
                            decres_qnty.quantity=  decres_qnty.quantity-order_item.quantity
                            decres_qnty.save()
                        cart_obj.delete()

                    return redirect('success',obj.id)
                except:
                    messages.error(request,'you have no balance in your wallet')
                    return redirect('showcart')
            
            


            # sel_adresss=request.POST.get('selected_user_id')
            # a=request.POST.get('selected_address')
            print(a,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            print(' print somthing')
            print(sel_adresss)
            # addrss=Address.objects.get(id=a)
            # print(addrss)
            print('paymetn handlerrrrrrrrrrrrrrrrrrrrrrrrrr okeyyyyyyyy')
            
            try:
                
                
                # get the required parameters from post request.
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                # verify the payment signature.
                result = razorpay_client.utility.verify_payment_signature(
				params_dict)

                if result is not None:
                    amount=t_amount
                    print(amount)
                    print(payment_id)
                    try:
                        # capture the payemt
                        razorpay_client.payment.capture(payment_id, amount)
                        print(amount)
                        
                        # save   the order to your database
                        if cart_obj:
                            obj=Order(
                                user=user,
                                total_amount=amount,
                                order_date=date,
                                payment_mode='razorpay'
                            )
                            obj.save()
                           
                            
                            for i in cart_obj:
                                order_item = Ordered_items(
                                    order_id=obj,
                                    product_name=i.product_id,
                                    user = obj.user.id,
                                    quantity = i.quantity,
                                    status = 'ordered',
                                    total_amount = i.total,
                                    expected_date = date + timedelta(days=8),
                                    addr_id='2',
                                    
                                )
                                order_item.save()
                            cart_obj.delete()

                        # render success page on successful caputre of payment
                        return redirect('success',obj.id)

                    except Exception as e :
                        print(e)
                        print('000000000000000000000000')
                        # if there is an error while capturing payment.
                        return render(request, 'paymentfail.html')
                else:
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    return render(request, 'paymentfail.html')

            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
            
    return redirect('user_login')



	

def apply_coupon(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=Customer.objects.get(email=email)
        t_amount=Cart.objects.filter(user_id=user).aggregate(total_price=Sum('total'))['total_price']

        # checkout=Checkout.objects.get(user=user)
        
        if request.method == "POST":
            code = request.POST.get("coupon_code")
            code = request.POST.get("coupon_code")
            if code.strip() == '':
                return JsonResponse({'error':  'please enter a coupon'})
            
            # checkout=Checkout.objects.get(user=user)
            
            # if checkout.coupon_active==True:
            #     return JsonResponse({'error':'you cannot add two coupon in one order'})
            try:
                coupon_database=Coupons.objects.get(code__iexact=code,active=True)
                date= timezone.now().date()
                if coupon_database.start_date > date:
                    return JsonResponse({'error':'coupon is not valid'})
                if coupon_database.end_date < date:
                    return JsonResponse({'error':'the coupon is expired'})
                if coupon_database.min_amount>t_amount:
                    return JsonResponse({'error':'amount should be more than your purchase amount'})
                if coupon_database.quantity <=0:
                    return JsonResponse({'error':'coupon quantity limit is reached'})

                else:
                    cart=Cart.objects.get(user_id=user)

                    if cart.coupon_active==False:
                        coupon_database.quantity -= 1
                        coupon_database.save()
                        cart.total-=coupon_database.discount_amount
                        cart.coupon_active=True
                        cart.save()
                        return JsonResponse({'error':'coupon applied'})
                    else:
                        return JsonResponse({'error':'coupon already applied'})
                # else:
                #     return JsonResponse({'error': 'Coupon is not available'})
            
            except Exception as e:
               
                
                return JsonResponse({'error':'Coupon not available'})
            
            
            return JsonResponse({'success': True, 'coupon_code': code})
        # return 



# def remove_coupen(request):
#     re