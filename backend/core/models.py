from django.db import models

class Subject(models.Model):
    code = models.CharField(max_length=20, unique = True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, blank = True, null=True)
    description = models.TextField(blank = True)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    subjects = models.ManyToManyField("Subject", related_name="teachers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
class Classroom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    grade_level = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    homeroom_teacher = models.ForeignKey(Teacher, related_name="homerooms", on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField("Subject", related_name="classrooms", blank=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["grade_level", "name"]
        constraints =[models.UniqueConstraint(fields=["grade_level", "name"], name = "uniq_grade_name")]

    def __str__(self):
        return f"{self.grade_level} - {self.name}"