from django.contrib import admin
from .models import Subject, Teacher, Classroom, Student, Enrollment, Attendance, Assignment, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "color", "created_at")
    list_filter = ("is_active", )
    search_fields = ("code", "name")

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "is_active", "hire_date")
    list_filter = ("is_active",)
    search_fields = ("first_name", "last_name", "email")

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "grade_level", "homeroom_teacher", "is_active" )
    list_filter = ("grade_level", "is_active")
    search_fields = ("name", )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "classroom", "is_active")
    list_filter = ("is_active", "gender", "classroom")
    search_fields = ("first_name", "last_name", "email", "guardian_name", "guardian_phone")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "teacher", "academic_year", "active")
    list_filter = ("academic_year", "active", "subject", "teacher")
    search_fields = ("academic_year", "student__first_name", "student__last_name", "subject__name", "subject__code", "teacher__first_name", "teacher__last_name",)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("date", "status", "enrollment", "recorded_by")
    list_filter = ("status", "date", "enrollment__subject", "enrollment__academic_year")
    search_fields = ("notes", "enrollment__student__first_name", "enrollment__student__last_name", "enrollment__subject__name", "enrollment__subject__code",)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "academic_year", "due_date", "max_points", "created_by")
    list_filter = ("academic_year", "subject", "due_date")
    search_fields = ("title", "description", "subject__name", "subject__code")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("assignment", "enrollment", "score", "graded_by", "submitted_at")
    list_filter = ("assignment__subject", "assignment__academic_year")
    search_fields = ("feedback", "enrollment__student__first_name", "enrollment__student__last_name", "asssignment__title", )