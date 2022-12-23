from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orderproduct/<int:id>', views.orderproduct, name='orderproduct'),
    path('ordercompleted', views.ordercompleted, name='ordercompleted'),
]