from django.contrib import admin
from .models import Subject, Teacher, Classroom

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