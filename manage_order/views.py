from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import *


# Create your views here.


@login_required(login_url='admin_login')
def admin_order(request):
    if 'email' in request.session:
        return render(request,'error.html')
    all_item=Ordered_items.objects.all().order_by('-id')
    contx={'all_item':all_item}
    return render(request,'orders.html',contx)

@login_required(login_url='admin_login')
def adm_order_det(request,id):
    prod_detail=Ordered_items.objects.get(id=id)
    contxx={'prod_detail':prod_detail}
    if request.method=='POST':
        change_status=request.POST.get('orderStatus')
        item=Ordered_items.objects.get(id=id)
        item.status=change_status
        item.save()
        return redirect('adm_order_det',id)
        
        print(id)
        print(item.product_name.name )
        print()

        # changed_sta=Ordered_items(status=change_status)
        # changed_sta.save()


    
    return render(request,'adm_order_det.html',contxx)


@login_required(login_url='admin_login')
def adm_return(request):
    if 'email' in request.session:
        return render(request,'error.html')
    returns = OrderReturns.objects.all().order_by('-id') 
    contx={'returns':returns}
    return render(request,'adm_return.html',contx )
