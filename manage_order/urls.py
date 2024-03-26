from django.urls import path
from . import views

urlpatterns = [
    path('admin_order',views.admin_order,name='admin_order'),
    path('adm_order_det/<str:id>',views.adm_order_det,name='adm_order_det'),
    path('adm_return',views.adm_return,name='adm_return')



]