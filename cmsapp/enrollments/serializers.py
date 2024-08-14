from rest_framework import serializers
from .models import Enrollment, Progress, CourseCompletion, Attendance
from courses.models import Course, Lesson  # Assuming you have related serializers for nested representation
from accounts.models import CustomUser
from django.utils import timezone
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['date_enrolled']  # Prevent date_enrolled from being edited after creation
        extra_kwargs = {
            'status': {'required': True},
        }

    def create(self, validated_data):
        # Automatically set the student from the request context
        request = self.context.get('request')
        validated_data['student'] = request.user if request else None
        return super().create(validated_data)

class ProgressSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ['date_completed']  # Auto-set when lesson is completed

    def update(self, instance, validated_data):
        # Automatically set date_completed if lesson is marked as completed
        if validated_data.get('completed'):
            validated_data['date_completed'] = timezone.now()
        return super().update(instance, validated_data)

class CourseCompletionSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseCompletion
        fields = '__all__'
        read_only_fields = ['completion_date']

    def validate_final_grade(self, value):
        # Custom validation for final grade
        if value and (value < 0.0 or value > 100.0):
            raise serializers.ValidationError("Final grade must be between 0 and 100.")
        return value

    def create(self, validated_data):
        # Automatically set the student from the request context
        request = self.context.get('request')
        validated_data['student'] = request.user if request else None
        return super().create(validated_data)

class AttendanceSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['attended_on']

    def create(self, validated_data):
        # Automatically set the student from the request context
        request = self.context.get('request')
        validated_data['student'] = request.user if request else None
        return super().create(validated_data)

    def validate_status(self, value):
        # Ensure the status is either 'present' or 'absent'
        if value not in ['present', 'absent']:
            raise serializers.ValidationError("Status must be either 'present' or 'absent'.")
        return value
