from django.contrib import admin
from .models import Subject, Teacher, Classroom, Student, Enrollment

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