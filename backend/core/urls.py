from django.urls import path, include
from .views import health, SubjectViewSet, TeacherViewSet, ClassroomViewSet, StudentViewSet, EnrollmentViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("subjects", SubjectViewSet, basename= "subject")
router.register("teachers", TeacherViewSet, basename= "teacher")
router.register("classrooms", ClassroomViewSet, basename= "classroom")
router.register("students", StudentViewSet, basename= "student")
router.register("enrollments", EnrollmentViewSet, basename= "enrollment")

urlpatterns = [
    path("health/" , health, name = "health"),
    path("", include(router.urls)),
]