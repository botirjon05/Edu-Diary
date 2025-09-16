from rest_framework import serializers
from .models import Subject, Teacher, Classroom

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class TeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(queryset = Subject.objects.all(), many = True, required = False)

    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class ClassroomSerializer(serializers.ModelSerializer):
    homeroom_teacher = serializers.PrimaryKeyRelatedField(queryset = Teacher.objects.all(), allow_null = True, required = False)
    subjects = serializers.PrimaryKeyRelatedField(queryset = Subject.objects.all(), many = True, required = False)

    class Meta:
        model = Classroom
        fields = "__all__"
        read_only_field = ("id", "created_at", "updated_at")

