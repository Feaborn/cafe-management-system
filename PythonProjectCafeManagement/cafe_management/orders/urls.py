from django.urls import path
from . import views
from .views import (
    OrderListCreateAPIView,
    OrderRetrieveUpdateDestroyAPIView,
    OrderSearchAPIView
)

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/new/', views.order_create, name='order_create'),
    path('order/<int:pk>/edit/', views.order_update, name='order_update'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('revenue/', views.revenue_report, name='revenue_report'),
    path('api/orders/', OrderListCreateAPIView.as_view(), name='order-api-list'),
    path('api/orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-api-detail'),
    path('api/orders/search/', OrderSearchAPIView.as_view(), name='order-api-search'),
]