from rest_framework import serializers
from django.utils import timezone
from .models import Assessment, Submission
from courses.models import Unit, LessonPlan, StudyMaterial

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name')

class LessonPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = ('id', 'title')

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ('id', 'title')

class AssessmentSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    lesson_plan = LessonPlanSerializer()
    study_materials = StudyMaterialSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ('id', 'name', 'description', 'course', 'unit', 'lesson_plan', 'study_materials', 'max_score', 'due_date', 'status', 'average_score', 'completion_rate')

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate_max_score(self, value):
        if value <= 0:
            raise serializers.ValidationError("Max score must be a positive number.")
        return value

    def update(self, instance, validated_data):
        unit_data = validated_data.pop('unit', None)
        lesson_plan_data = validated_data.pop('lesson_plan', None)
        study_materials_data = validated_data.pop('study_materials', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle nested updates if necessary
        if unit_data:
            # Update or create unit
            pass  # Implement update logic if needed

        if lesson_plan_data:
            # Update or create lesson plan
            pass  # Implement update logic if needed

        if study_materials_data:
            # Update or create study materials
            pass  # Implement update logic if needed

        return instance

class SubmissionSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all())
    feedback = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Submission
        fields = ('id', 'student', 'assessment', 'submitted_on', 'content', 'file', 'grade', 'feedback')

    def validate_submitted_on(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Submission date cannot be in the future.")
        return value

    def validate_grade(self, value):
        if value is not None and (value < 0 or value > self.instance.assessment.max_score):
            raise serializers.ValidationError("Grade must be between 0 and the maximum score.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['formatted_date'] = instance.submitted_on.strftime('%Y-%m-%d %H:%M:%S')
        return representation
