from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('user_manage/',views.user_manage,name='user_manage'),
    path('userunblock/<str:id>',views.userunblock,name='userunblock'),
    path('userblock/<str:id>',views.userblock,name='userblock')
   
]