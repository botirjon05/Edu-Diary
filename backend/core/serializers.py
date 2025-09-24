from rest_framework import serializers
from .models import Subject, Teacher, Classroom, Student, Enrollment, Attendance, Assignment, Grade, Announcement

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
        read_only_fields = ("id", "created_at", "updated_at")

class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset = Classroom.objects.all(), allow_null = True, required = False)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset = Student.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset = Subject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset = Teacher.objects.all(), allow_null = True, required = False) 

    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        return attrs
    
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
        read_only_fields = ("id", "submitted_at")

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        assignment = attrs.get("assignment") or (getattr(instance, "assignment", None))
        enrollment = attrs.get("enrollment") or (getattr(instance, "enrollment", None))

        if not assignment or not enrollment:
            return attrs

        if assignment.subject_id != enrollment.subject_id:
            raise serializers.ValidationError("Assignment subject and enrollment subject must match")
        if assignment.academic_year != enrollment.academic_year:
            raise serializers.ValidationError("Assignment year and enrollment year must match")
        
        score = attrs.get("score")
        if score is not None and score > assignment.max_points:
            raise serializers.ValidationError("Score cannot exceed assignment max_points")
        return attrs
    

class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = "created_by.username")
    subject_name = serializers.ReadOnlyField(source = "subject.name")

    class Meta: 
        model = Announcement
        fields = ["id", "subject", "subject_name", "title", "body", "is_pinned", "visible_from", "visible_to", "author", "created_at", "updated_at", ]
        read_only_fields = ("author", "created_at", "updated_at")

    def validate(self, attrs):
        start = attrs.get("visible_from")
        end = attrs.get("visible_to")
        if start and end and end < start:
            raise serializers.ValidationError("visible_to must be after visible_from")
        return attrs
    
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)