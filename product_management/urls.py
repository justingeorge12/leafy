from . import views
from django.urls import path

urlpatterns = [
    path('product/',views.product,name='product'),
    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<str:id>',views.edit_product,name='edit_product'),
    path('list_pro/<str:id>',views.list_pro,name='list_pro'),
    path('unlist_pro/<str:id>',views.unlist_pro,name='unlist_pro'),
    path('edit_varint',views.edit_varint,name='edit_varint')
]
