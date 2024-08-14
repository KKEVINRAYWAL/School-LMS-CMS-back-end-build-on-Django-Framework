from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from courses.models import Course
from assessments.models import Assessment

CustomUser = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'bio']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'code', 'semester', 'credits', 'instructor']

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'name', 'description', 'course', 'max_score', 'due_date']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    courses = CourseSerializer(many=True, required=False)
    assessments = AssessmentSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_student', 'is_instructor', 'profile', 'courses', 'assessments']
        read_only_fields = ['id']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        courses_data = validated_data.pop('courses', [])
        assessments_data = validated_data.pop('assessments', [])

        user = CustomUser.objects.create(**validated_data)

        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)

        # Handle courses and assessments
        for course_data in courses_data:
            user.courses.add(Course.objects.get(id=course_data['id']))
        for assessment_data in assessments_data:
            user.assessments.add(Assessment.objects.get(id=assessment_data['id']))

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        courses_data = validated_data.pop('courses', [])
        assessments_data = validated_data.pop('assessments', [])

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_student = validated_data.get('is_student', instance.is_student)
        instance.is_instructor = validated_data.get('is_instructor', instance.is_instructor)
        instance.save()

        if profile_data:
            UserProfile.objects.update_or_create(user=instance, defaults=profile_data)

        # Update courses and assessments
        if courses_data:
            instance.courses.set([Course.objects.get(id=course['id']) for course in courses_data])
        if assessments_data:
            instance.assessments.set([Assessment.objects.get(id=assessment['id']) for assessment in assessments_data])

        return instance
