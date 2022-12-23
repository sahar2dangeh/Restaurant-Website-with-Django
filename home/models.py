from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.forms import ModelForm, TextInput, Textarea


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=255)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=50)
    smtpport = models.CharField(blank=True, max_length=50)
    icon = models.ImageField(blank=True, upload_to='images//')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField()
    contact = RichTextUploadingField()
    references = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'نام و نام خانوادگی '}),
            'subject': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'موضوع '}),
            'email': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'ایمیل '}),
            'message': Textarea(attrs={'class': 'bo-rad-10 size35 bo2 txt10 p-l-20 p-t-15 m-b-10 m-t-3', 'placeholder': 'پیغام شما', 'rows': '5'}),
        }


class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=150)
    answer = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question