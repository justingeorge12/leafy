from django.urls import path
from . import views

urlpatterns = [
    path('user_profile',views.user_profile,name='user_profile'),
    path('change_pass/',views.change_pass,name='change_pass'),
    path('add_address/',views.add_address,name='add_address'),
    path('delete_add/<str:id>',views.delete_add,name='delete_add'),
    path('edit_pro/<str:id>',views.edit_pro,name='edit_pro'),
    path('edit_add/<str:id>',views.edit_add,name='edit_add'),
    path('order_detail/<str:id>',views.order_detail,name='order_detail'),
    path('cancel_order/<str:id>',views.cancel_order,name='cancel_order'),
    path('return_order/<str:id>',views.return_order,name='return_order'),
     
    
   
]
