from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Subject, Teacher, Classroom
from .serializers import SubjectSerializer, TeacherSerializer, ClassroomSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"ok": True, "app": "Edu Diary API"})

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all().order_by("name")
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["is_active"]
    search_fields = ["code", "name", "description"]
    ordering_fields = ["name", "code", "created_at"]
    ordering = ["name"]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().select_related().prefetch_related("subjects")
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_active", "subjects"]
    search_fields = ["first_name", "last_name", "email", "phone"]
    ordering_fields = ["last_name", "first_name", "hire_date", "created_at"]
    ordering = ["last_name", "first_name"]

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all().select_related("homeroom_teacher").prefetch_related("subjects")
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_active", "grade_level", "subjects", "homeroom_teacher"]
    search_fields = ["name"]
    ordering_fields = ["grade_level", "name", "created_at"]
    ordering = ["grade_level", "name"]
