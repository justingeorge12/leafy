from django.urls import path
from . import views

urlpatterns = [
    path('addtocart/<str:id>',views.addtocart,name='addtocart'),
    path('showcart/',views.showcart,name='showcart'),
    path('update_quant/',views.update_quant,name='update_quant'),
    # path('checkout/<str:id>',views.checkout,name='checkout'),
    # path('place_oder',views.place_oder,name='place_oder'),
    path('remove/<str:id>',views.remove,name='remove'),
    path('add_addrs',views.add_addrs,name='add_addrs'),
    # path('razorpay',views.razorpay,name='razorpay'),
    path('placeorder/<str:id>',views.placeorder,name='placeorder'),
    path('success/<str:id>/',views.success,name='success'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    # path('checkk',views.checkk,name='checkk')
    # path('cod',views.cod,name='cod')
    # path('remove_coupen',views.remove_coupen,name='remove_coupen'),

    


]