from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from product.models import Product


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('On Serving', 'On Serving'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    table_no = models.IntegerField()
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    note = models.CharField(blank=True, max_length=100)
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.table_no)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table_no']


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    amount = models.FloatField()
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    note = models.CharField(blank=True, max_length=100)
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['amount']