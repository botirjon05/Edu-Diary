from django.urls import path, include
from .views import health, SubjectViewSet, TeacherViewSet, ClassroomViewSet, StudentViewSet, EnrollmentViewSet, AttendanceViewSet, AssignmentViewSet, GradeViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("subjects", SubjectViewSet, basename= "subject")
router.register("teachers", TeacherViewSet, basename= "teacher")
router.register("classrooms", ClassroomViewSet, basename= "classroom")
router.register("students", StudentViewSet, basename= "student")
router.register("enrollments", EnrollmentViewSet, basename= "enrollment")
router.register("attendance", AttendanceViewSet, basename= "attendance")
router.register("assignments", AssignmentViewSet, basename= "assignment")
router.register("grades", GradeViewSet, basename= "grade")

urlpatterns = [
    path("health/" , health, name = "health"),
    path("", include(router.urls)),
]