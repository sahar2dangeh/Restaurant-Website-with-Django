from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from product.models import CommentForm, Comment, Product


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "نظر شما با موفقیت ارسال شد. با تشکر.")
            return HttpResponseRedirect(url)
    messages.warning(request, "نظر شما ارسال نشد.")
    return HttpResponseRedirect(url)
