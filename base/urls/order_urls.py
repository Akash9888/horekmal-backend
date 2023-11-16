from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('add/', views.addOrderItems, name='add-orders'),
    path('<int:pk>/',views. getOrderById,name='get-order'),
    path('<int:pk>/pay/',views. updateOrderToPaid,name='pay-order'),
    path('',views.getOrders,name="get-orders")
]
