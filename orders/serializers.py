from rest_framework import serializers
from .models import Order, OrderItem, OrderLog


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_sku', 'product_image', 
                 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'total_price']


class OrderLogSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    
    class Meta:
        model = OrderLog
        fields = ['id', 'action', 'description', 'operator_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    logs = OrderLogSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'status_display',
            'user', 'user_name',
            'receiver_name', 'receiver_phone', 'receiver_address',
            'total_amount', 'discount_amount', 'shipping_fee', 'final_amount',
            'notes',
            'created_at', 'updated_at', 'paid_at', 'shipped_at', 'delivered_at',
            'items', 'logs'
        ]
        read_only_fields = [
            'id', 'order_number', 'user', 'created_at', 'updated_at',
            'paid_at', 'shipped_at', 'delivered_at'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'receiver_name', 'receiver_phone', 'receiver_address',
            'notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        order = Order.objects.create(user=user, **validated_data)
        
        total_amount = 0
        for item_data in items_data:
            item = OrderItem.objects.create(order=order, **item_data)
            total_amount += item.total_price
        
        order.total_amount = total_amount
        order.final_amount = total_amount + order.shipping_fee - order.discount_amount
        order.save()
        
        # 创建订单日志
        OrderLog.objects.create(
            order=order,
            action='CREATE',
            description='订单创建成功',
            operator=user
        )
        
        return order


class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data['status']
        notes = validated_data.get('notes', '')
        
        instance.status = new_status
        
        # 根据状态设置时间字段
        if new_status == 'paid' and not instance.paid_at:
            from django.utils import timezone
            instance.paid_at = timezone.now()
        elif new_status == 'shipped' and not instance.shipped_at:
            from django.utils import timezone
            instance.shipped_at = timezone.now()
        elif new_status == 'delivered' and not instance.delivered_at:
            from django.utils import timezone
            instance.delivered_at = timezone.now()
        
        instance.save()
        
        # 创建状态变更日志
        OrderLog.objects.create(
            order=instance,
            action='STATUS_CHANGE',
            description=f'订单状态从 {dict(Order.STATUS_CHOICES)[old_status]} 变更为 {dict(Order.STATUS_CHOICES)[new_status]}。{notes}',
            operator=self.context['request'].user
        )
        
        return instance