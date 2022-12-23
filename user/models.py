from django.db import models
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def user_image(self):
        return self.image

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' ' + '[' + self.user.username + ']'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    image_tag.short_description = 'Image'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']