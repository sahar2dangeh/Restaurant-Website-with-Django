import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.forms import SearchForm
from home.models import Setting, ContactForm, ContactFormMessage, FAQ
from user.models import UserProfile
from product.models import Product, Category, Images, Comment


def index(request):
    sliderData = Product.objects.filter(status='True').order_by('id')[:3]
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    ourFavorites = sorted(Product.objects.filter(status='True'), key=lambda i: -i.avaragecomment())[:3]
    ourLatestDeliciousFoods = Product.objects.filter(status='True').order_by('-id')[:3]
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {
        'setting': setting,
        'category': category,
        'page': 'home',
        'sliderData': sliderData,
        'ourFavorites': ourFavorites,
        'ourLatestDeliciousFoods': ourLatestDeliciousFoods,
        'profile': profile,
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'aboutus'}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'references'}
    return render(request, 'references.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            if data.name and data.email and data.subject and data.message:
                messages.success(request, "پیام شما با موفقیت ارسال شد. با تشکر.")
                data.save()
            else:
                messages.warning(request, "لطفا فرم را پر کنید و سعی کنید دوباره ارسال کنید.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    form = ContactForm()
    context = {'setting': setting, 'category': category, 'profile': profile, 'form': form}
    return render(request, 'contact.html', context)


def faq(request):
    setting = Setting.objects.get(pk=1, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    faq = FAQ.objects.filter(status='True').order_by('ordernumber')
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'faq': faq, 'page': 'faq'}
    return render(request, 'faq.html', context)


def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1, status='True')
    products = Product.objects.filter(category_id=id, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    categorydata = Category.objects.get(pk=id, status='True')
    context = {'setting': setting, 'products': products, 'category': category, 'profile': profile, 'categorydata': categorydata}
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    setting = Setting.objects.get(pk=1, status='True')
    product = Product.objects.get(pk=id, status='True')
    category = Category.objects.filter(status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'setting': setting, 'category': category, 'product': product, 'profile': profile, 'images': images, 'comments': comments}
    return render(request, 'product_detail.html', context)


def product_search(request):
    setting = Setting.objects.get(pk=1, status='True')
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.filter(status='True')
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query, status='True')
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid, status='True')
            context = {'setting': setting, 'products': products, 'profile': profile, 'category': category}
            return render(request, 'product_search.html', context)
    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q, status='True')
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
