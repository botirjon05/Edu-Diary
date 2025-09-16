from django.urls import path, include
from .views import health, SubjectViewSet, TeacherViewSet, ClassroomViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("subjects", SubjectViewSet, basename= "subject")
router.register("teachers", TeacherViewSet, basename= "teacher")
router.register("classrooms", ClassroomViewSet, basename= "classroom")

urlpatterns = [
    path("health/" , health, name = "health"),
    path("", include(router.urls)),
]