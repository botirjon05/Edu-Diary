from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Subject
from .serializers import SubjectSerializer

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
