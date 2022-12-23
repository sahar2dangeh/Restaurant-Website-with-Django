from django.contrib import admin

from order.models import Order, OrderProduct


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'amount', 'total', 'ip')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['table_no', 'total', 'note', 'ip', 'status']
    list_filter = ['table_no']
    readonly_fields = ('user', 'table_no', 'total', 'ip')
    can_delete = False
    inlines = [OrderProductLine]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'amount', 'total']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)