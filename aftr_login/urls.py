from . import views
from django.urls import path


urlpatterns = [
    path('one_product/<str:id>',views.one_product,name='one_product'),
    path('drop_category/<str:id>',views.drop_category,name='drop_category'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtowish/<str:id>/<str:frompage>',views.addtowish,name='addtowish'),
    path('deletewish/<str:id>',views.deletewish,name='deletewish'),
    path('movetocart/<str:id>',views.movetocart,name='movetocart'),

    
]
