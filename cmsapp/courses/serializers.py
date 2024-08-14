from rest_framework import serializers
from .models import Course, Unit, Lesson, LessonPlan, StudyMaterial, Enrollment, Progress
from content.models import Content, Assignment

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ['id', 'title', 'file', 'description']

class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = ['id', 'objectives', 'materials_needed', 'lesson_procedure', 'assessment_methods', 'lesson_reflection']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'content_type', 'file', 'url', 'tags', 'created_at', 'released_at']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'file_submission', 'text_submission']

class LessonSerializer(serializers.ModelSerializer):
    lesson_plan = LessonPlanSerializer(read_only=True)
    study_materials = StudyMaterialSerializer(many=True, read_only=True)
    contents = ContentSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'schedule_date', 'start_time', 'end_time', 'lesson_plan', 'study_materials', 'contents', 'assignments']

class UnitSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ['id', 'name', 'description', 'course', 'required_for_completion', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    instructor = serializers.StringRelatedField()  # To show instructor's name instead of ID

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'semester', 'instructor', 'units']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'date_enrolled']

class ProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'student', 'lesson', 'completed', 'date_completed']
