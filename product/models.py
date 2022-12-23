from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models.functions import Coalesce

# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    slug = models.SlugField(null=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def avaragecomment(self):
        comments = Comment.objects.filter(product=self).aggregate(avarage=Avg('rate'))
        avg = 0
        if comments["avarage"] is not None:
            avg = float(comments["avarage"])
        return avg


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']