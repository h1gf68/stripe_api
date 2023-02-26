from django.contrib import admin
from payments.models import Item, Order, OrderItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    exclude = ['checkout_session']
    inlines = [OrderItemInline]


class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'price', 'quantity']


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemModelAdmin)
