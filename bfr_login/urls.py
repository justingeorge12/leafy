from . import views
from django.urls import path


urlpatterns = [
    path('',views.home,name='home'),
    path('gallery/',views.gallery,name='gallery'),
    path('about_us/',views.about_us,name='about_us'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('login/',views.user_login,name='user_login'),
    path('register/',views.register,name='register'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('otp_verif/<str:id>',views.otp_verif,name='otp_verif'),
    path('shop/',views.shop,name='shop'),
    path('forget_pass',views.forget_pass,name='forget_pass'),
    path('forget_otp/<str:id>',views.forget_otp,name='forget_otp'),
    path('reset_pass/<str:id>',views.reset_pass,name='reset_pass'),
    
    
]

