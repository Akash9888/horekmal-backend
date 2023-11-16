from django.urls import path
from base.views import payment_views as views


urlpatterns = [
    path('',views.payment,name='payment'),
]