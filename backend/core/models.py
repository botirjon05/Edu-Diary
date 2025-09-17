from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    email = models.EmailField(unique=True, null =True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    guardian_name = models.CharField(max_length=120, blank=True)
    guardian_phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    classroom = models.ForeignKey("Classroom", related_name="students", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
class Enrollment(models.Model):
    student = models.ForeignKey("Student", related_name="enrollments", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", related_name="enrollments", on_delete=models.CASCADE)
    teacher = models.ForeignKey("Teacher", related_name="enrollments", on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.CharField(max_length=9)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-academic_year", "student__last_name", "subject__name"]
        constraints = [models.UniqueConstraint(fields= ["student", "subject", "academic_year"], name="uniq_enrollment_student_subject_year", )]

    def __str__(self) -> str:
        return f"{self.student} → {self.subject} ({self.academic_year})"
    
class Attendance (models.Model):
    class Status(models.TextChoices):
        PRESENT = "P", "Present"
        ABSENT = "A", "Absent"
        LATE = "L", "Late"
        EXCUSED = "E", "Excused"

    enrollment = models.ForeignKey("Enrollment", related_name="attendance", on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PRESENT)
    notes = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey("Teacher", related_name="attendance_records", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "enrollment__student__last_name"]
        constraints = [models.UniqueConstraint(fields=["enrollment", "date"], name="uniq_attendance_enrollment_date")]
        indexes = [models.Index(fields=["date"]), models.Index(fields=["status"]),]

    def __str__(self):
        s = self.get_status_display()
        return f"{self.enrollment} @ {self.date} → {s}"
    
class Assignment(models.Model):
    subject = models.ForeignKey("Subject", related_name= "assignments", on_delete= models.CASCADE)
    academic_year = models.CharField(max_length=9)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    max_points = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1)])
    created_by = models.ForeignKey("Teacher", related_name="created_assignments", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-due_date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.subject.code})"
    
class Grade(models.Model):
    assignment = models.ForeignKey("Assignment", related_name="grades", on_delete=models.CASCADE)
    enrollment = models.ForeignKey("Enrollment", related_name="grades", on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    feedback = models.CharField(max_length=255, blank=True)
    graded_by = models.ForeignKey("Teacher", related_name="grades_given", on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [models.UniqueConstraint(fields=["assignment", "enrollment"], name = "uniq_grade_assignment_enrollment")]

    def __str__(self):
        return f"{self.enrollment} → {self.assignment}: {self.score}"
    


 
