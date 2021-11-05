from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    fields = ('plant', 'quantity', 'total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)
    readonly_fields = ('order_uuid', 'date', 'total_cost', 'stripe_pid',)
    fields = (
        'order_uuid', 'date', 'first_name', 'last_name', 'email',
        'address', 'city', 'postcode', 'country', 'phone_number',
        'total_cost', 'stripe_pid',)
    list_display = (
        'order_uuid', 'date', 'first_name', 'last_name', 'total_cost',)
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
