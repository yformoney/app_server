from django.contrib import admin
from .models import Order, OrderItem, OrderLog


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


class OrderLogInline(admin.TabularInline):
    model = OrderLog
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'final_amount', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__username', 'receiver_name', 'receiver_phone']
    readonly_fields = ['id', 'order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline, OrderLogInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('id', 'order_number', 'user', 'status')
        }),
        ('收货信息', {
            'fields': ('receiver_name', 'receiver_phone', 'receiver_address')
        }),
        ('金额信息', {
            'fields': ('total_amount', 'discount_amount', 'shipping_fee', 'final_amount')
        }),
        ('备注信息', {
            'fields': ('notes',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'total_price']
    list_filter = ['created_at']
    search_fields = ['product_name', 'product_sku', 'order__order_number']
    readonly_fields = ['total_price']


@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    list_display = ['order', 'action', 'operator', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['order__order_number', 'description', 'operator__username']
    readonly_fields = ['created_at']