from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from order.models import Order, OrderProduct
from user.models import UserProfile
from home.models import Setting
from product.models import Category, Comment
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'userprofile'}
    return render(request, 'user_profile.html', context)


def logout_view(request):
    logout(request)
    request.session['table_no'] = None
    request.session['order_id'] = None
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['table_no'] = None
            request.session['order_id'] = None
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "نام کاربری یا رمز عبور شما صحیح نیست.")
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'login'}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password1 = request.POST['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            return HttpResponseRedirect('/')

    form = SignUpForm()
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'form': form, 'page': 'login'}
    return render(request, 'signup.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'حساب شما به روز شده است!')
            return HttpResponseRedirect('/user')
    else:
        setting = Setting.objects.get(pk=1, status='True')
        current_user = request.user
        if current_user.id is not None:
            profile = UserProfile.objects.get(user_id=current_user.id)
        else:
            profile = None
        category = Category.objects.filter(status='True')
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'setting': setting,
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'رمز عبور شما با موفقیت به روز شد!')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, 'لطفا خطای زیر را اصلاح کنید.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        setting = Setting.objects.get(pk=1, status='True')
        category = Category.objects.filter(status='True')
        current_user = request.user
        if current_user.id is not None:
            profile = UserProfile.objects.get(user_id=current_user.id)
        else:
            profile = None
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
            'category': category,
            'setting': setting,
            'profile': profile,
        }
        return render(request, 'user_password.html', context)


@login_required(login_url='/login')
def orders(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    orders = Order.objects.filter(user_id=current_user.id).order_by('-create_at')
    context = {
        'orders': orders,
        'category': category,
        'setting': setting,
        'profile': profile,
    }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')
def orderdetail(request, id):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderItems = OrderProduct.objects.filter(order_id=id).order_by('-create_at')
    context = {
        'order': order,
        'orderItems': orderItems,
        'category': category,
        'setting': setting,
        'profile': profile,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')
def comments(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    comments = Comment.objects.filter(user_id=current_user.id).order_by('-create_at')
    context = {
        'comments': comments,
        'category': category,
        'setting': setting,
        'profile': profile,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'نظر شما حذف شد.')
    return HttpResponseRedirect('/user/comments')

