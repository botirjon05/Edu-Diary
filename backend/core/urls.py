from django.urls import path 
from .views import health
from . import views

urlpatterns = [
    path("health/" , health, name = "health"),
]