from rest_framework import serializers
from .models import Content, Assignment, ContentVersion, Interaction
from django.utils import timezone
class ContentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentVersion
        fields = ['id', 'content', 'version_number', 'file', 'url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'user', 'content', 'interaction_type', 'timestamp']

class ContentSerializer(serializers.ModelSerializer):
    versions = ContentVersionSerializer(many=True, read_only=True)
    interactions = InteractionSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'course', 'unit', 'content_type', 'current_version', 'tags', 'release_date', 'versions', 'interactions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'versions', 'interactions']

    def validate(self, data):
        """
        Custom validation to ensure either file or url is provided based on content type.
        """
        content_type = data.get('content_type')
        if content_type in ['video', 'pdf', 'text'] and not data.get('file') and not data.get('url'):
            raise serializers.ValidationError("Content of type '{}' requires either a file or a URL.".format(content_type))
        return data

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'course', 'unit', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_due_date(self, value):
        """
        Validate that due date is not in the past.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
