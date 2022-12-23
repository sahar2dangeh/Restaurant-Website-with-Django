from django.contrib import admin

from home.models import Setting, ContactFormMessage, FAQ


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'note', 'status']
    list_filter = ['status']
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip',)


class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'answer', 'status']
    list_filter = ['status']


admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
admin.site.register(Setting)
admin.site.register(FAQ, FAQAdmin)