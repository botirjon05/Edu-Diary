from django.urls import path, include
from .views import health, SubjectViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("subjects", SubjectViewSet, basename= "subject")

urlpatterns = [
    path("health/" , health, name = "health"),
    path("", include(router.urls)),
]