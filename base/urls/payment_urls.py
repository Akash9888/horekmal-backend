from django.urls import path
from base.views import payment_views as views

urlpatterns = [
    path('ssl-session/', views.get_ssl_session, name='ssl-session'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
    path('cancel/', views.cancel, name='cancel'),
]
