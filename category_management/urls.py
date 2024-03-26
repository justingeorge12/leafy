from . import views
from django.urls import path

urlpatterns = [
    path('category/',views.category,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('edit_category/<str:id>',views.edit_category,name='edit_category'),
    path('unlist_cate/<str:id>',views.unlist_cate,name='unlist_cate'),
    path('list_cate/<str:id>',views.list_cate,name='list_cate'),
    
]
