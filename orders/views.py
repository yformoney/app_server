from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import Order, OrderLog
from .serializers import (
    OrderSerializer, CreateOrderSerializer, 
    UpdateOrderStatusSerializer, OrderLogSerializer
)


class OrderViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'update_status':
            return UpdateOrderStatusSerializer
        return OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        
        # 状态筛选
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # 日期范围筛选
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                from datetime import datetime, time
                end_datetime = datetime.combine(end_date, time.max)
                queryset = queryset.filter(created_at__lte=end_datetime)
        
        # 订单号搜索
        order_number = self.request.query_params.get('order_number')
        if order_number:
            queryset = queryset.filter(order_number__icontains=order_number)
        
        return queryset.prefetch_related('items', 'logs').select_related('user')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            response_serializer = OrderSerializer(order)
            return Response({
                'success': True,
                'message': '订单创建成功',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': '订单创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_order = serializer.save()
            response_serializer = OrderSerializer(updated_order)
            return Response({
                'success': True,
                'message': '订单状态更新成功',
                'data': response_serializer.data
            })
        
        return Response({
            'success': False,
            'message': '订单状态更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        if order.status not in ['pending', 'paid']:
            return Response({
                'success': False,
                'message': '该订单状态不允许取消'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        
        # 创建取消订单日志
        OrderLog.objects.create(
            order=order,
            action='CANCEL',
            description='用户取消订单',
            operator=request.user
        )
        
        serializer = OrderSerializer(order)
        return Response({
            'success': True,
            'message': '订单取消成功',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        user_orders = Order.objects.filter(user=request.user)
        
        stats = {
            'total_orders': user_orders.count(),
            'pending_orders': user_orders.filter(status='pending').count(),
            'paid_orders': user_orders.filter(status='paid').count(),
            'processing_orders': user_orders.filter(status='processing').count(),
            'shipped_orders': user_orders.filter(status='shipped').count(),
            'delivered_orders': user_orders.filter(status='delivered').count(),
            'cancelled_orders': user_orders.filter(status='cancelled').count(),
        }
        
        return Response({
            'success': True,
            'data': stats
        })


class OrderLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            logs = OrderLog.objects.filter(order=order)
            serializer = OrderLogSerializer(logs, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Order.DoesNotExist:
            return Response({
                'success': False,
                'message': '订单不存在'
            }, status=status.HTTP_404_NOT_FOUND)