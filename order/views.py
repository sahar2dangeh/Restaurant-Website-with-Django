from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from home.models import Setting
from user.models import UserProfile
from order.models import OrderForm, Order, OrderProduct, OrderProductForm
from product.models import Category, Product


def index(request):
    return HttpResponse("Order App")


def ordercompleted(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'ordercompleted'}
    return render(request, 'ordercompleted.html', context)


@login_required(login_url='/login')
def orderproduct(request, id):
    if not request.session.get('table_no'):
        request.session['table_no'] = None
        request.session['order_id'] = None
    category = Category.objects.filter(status='True')
    current_user = request.user
    total = 0
    if request.method == 'POST':
        data = None
        total = 0
        form = OrderForm(request.POST)
        form2 = OrderProductForm(request.POST)
        if form.is_valid():
            if request.session['table_no'] is None:
                data = Order()
                request.session['table_no'] = form.cleaned_data['table_no']
                data.table_no = form.cleaned_data['table_no']
            else:
                data = Order.objects.get(id=request.session['order_id'])
                data.table_no = request.session['table_no']
        else:
            if request.session['table_no'] is None:
                data = Order()
            else:
                data = Order.objects.get(id=request.session['order_id'])
        if form2.is_valid():
            data.user_id = current_user.id
            data.ip = request.META.get('REMOTE_ADDR')
            detail = OrderProduct()
            detail.product_id = id
            detail.amount = form2.cleaned_data['amount']
            detail.price = Product.objects.get(id=detail.product_id).price
            total += Product.objects.get(id=detail.product_id).price * detail.amount
            detail.total = total
            if data.total is not None:
                data.total += total
            else:
                data.total = total
            data.save()
            if request.session['order_id'] is not None:
                detail.order_id = request.session['order_id']
            else:
                request.session['order_id'] = data.id
                detail.order_id = data.id
            detail.user_id = data.user_id
            detail.ip = data.ip
            detail.save()
            #messages.success(request, "Your Order has been completed. Thank you ")
            return HttpResponseRedirect('/order/ordercompleted')
        else:
            messages.warning(request, form.errors)
    return redirect(request.META.get('HTTP_REFERER'))
