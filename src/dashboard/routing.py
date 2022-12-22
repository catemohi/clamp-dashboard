from django.urls import path

from .consumers import DashboardConsumer

ws_urlpatterns = [
    path('ws/log/', DashboardConsumer.as_asgi())
]
