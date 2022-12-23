from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from user.models import UserProfile
from django.forms import TextInput, EmailInput, Select, FileInput


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='نام کاربری', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    email = forms.EmailField(max_length=200, label='ایمیل', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    first_name = forms.CharField(max_length=100, label='نام', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    last_name = forms.CharField(max_length=100, label='نام خانوادگی', widget=forms.TextInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    password1 = forms.CharField(max_length=100, label='گذرواژه', widget=forms.PasswordInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))
    password2 = forms.CharField(max_length=100, label='تایید گذرواژه', widget=forms.PasswordInput(attrs={'class': "bo-rad-10 sizefull txt10 p-l-20"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        widgets = {
            'username': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'نام کاربری'}),
            'email': EmailInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'last_name'}),
            'password': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'value': 'aa'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Bursa', 'Bursa'),
    ('London', 'London'),
    ('New York', 'New York'),
    ('Tokyo', 'Tokyo'),
    ('Paris', 'Paris'),
    ('Moscow', 'Moscow'),
    ('Rome', 'Rome'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'شماره تماس'}),
            'address': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'نشانی'}),
            'city': Select(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'شهر'}, choices=CITY),
            'country': TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'کشور'}),
            'image': FileInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20 p-t-10', 'placeholder': 'image', }),
        }