from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderLogView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/<uuid:order_id>/logs/', OrderLogView.as_view(), name='order-logs'),
]