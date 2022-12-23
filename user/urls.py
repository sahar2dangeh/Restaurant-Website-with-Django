from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='user_password'),
    path('orders/', views.orders, name='user_orders'),
    path('orderdetail/<int:id>', views.orderdetail, name='orderdetail'),
    path('comments/', views.comments, name='user_comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='user_deletecomment'),
]