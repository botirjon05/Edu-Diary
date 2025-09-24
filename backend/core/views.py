from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .models import Subject, Teacher, Classroom, Student, Enrollment, Attendance, Assignment, Grade
from .serializers import SubjectSerializer, TeacherSerializer, ClassroomSerializer, StudentSerializer, EnrollmentSerializer, AttendanceSerializer, AssignmentSerializer, GradeSerializer

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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related("classroom")
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_active", "gender", "classroom"]
    search_fields = ["first_name", "last_name", "email", "phone","guardian_name", "guardian_phone"]
    ordering_fields = ["last_name", "first_name", "date_of_birth", "created_at"]
    ordering = ["last_name", "first_name"]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().select_related("student", "subject", "teacher")
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["active", "academic_year", "student", "subject", "teacher"]
    search_fields = ["academic_year", "student__first_name", "student__last_name", "subject__name", "subject__code", "teacher__first_name", "teacher__last_name", ]
    ordering_fields = ["academic_year", "created_at", "updated_at"]
    ordering = ["-academic_year", "student__last_name"]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("enrollment", "enrollment__student", "enrollment__subject", "recorded_by").all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "date", "enrollment__student", "enrollment__subject", "enrollment__academic_year", ]
    search_fields = ["notes", "enrollment__student__first_name", "enrollment__student__last_name", "enrollment__subject__name", "enrollment__subject__code",]
    ordering_fields = ["date", "created_at", "updated_at"]
    ordering = ["-date"]

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        qs = self.filter_queryset(self.get_queryset())
        total = qs.count()
        present = qs.filter(status = Attendance.Status.PRESENT).count()
        late = qs.filter(status = Attendance.Status.LATE).count()
        absent = qs.filter(status = Attendance.Status.ABSENT).count()
        excused = qs.filter(status = Attendance.Status.EXCUSED).count()
        rate = (present/total) * 100 if total else 0.0
        return Response({"total": total, "present": present, "late": late, "absent": absent, "excused": excused, "present_rate_pct": round(rate, 2),})
    
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related("subject", "created_by").all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["subject", "academic_year", "due_date", "created_by"]
    search_fields = ["title", "description", "subject__name", "subject__code"]
    ordering_fields = ["due_date", "created_at", "updated_at", "max_points"]
    ordering = ["-due_date"]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related("assignment", "assignment__subject", "enrollment", "enrollment__student", "enrollment__subject", "graded_by",).all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["assignment", "assignment__subject", "assignment__academic_year", "enrollment", "enrollment__student", "enrollment__subject", ]
    search_fields = ["feedback", "enrollment__student__first_name", "enrollment__student__last_name", "assignment__title", ]
    ordering_fields = ["submitted_at", "score"]
    ordering = ["-submitted_at"]

    @action(detail=False, methods=["get"], url_path="avg")
    def average(self, request):
        qs = self.filter_queryset(self.get_queryset())
        by_student = {}
        for g in qs:
            sid = g.enrollment.student_id
            by_student.setdefault(sid, []).append(float(g.score))
        avgs = {str(sid): round(sum(v)/len(v), 2) for sid, v in by_student.items() if v}
        return Response({"count": qs.count(), "averages": avgs})
    
    def perform_create(self, serializer):
        serializer.save(graded_by = self.request.user)
