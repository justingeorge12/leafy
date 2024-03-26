from . import views
from django.urls import path


urlpatterns = [
    path('view_coupon',views.view_coupon,name='view_coupon'),
    path('create_coupon',views.create_coupon,name='create_coupon'),
    path('inactive/<str:id>',views.inactive,name='inactive'),
    path('active/<str:id>',views.active,name='active'),
    path('edit_coupon/<str:id>',views.edit_coupon,name='edit_coupon'),
]