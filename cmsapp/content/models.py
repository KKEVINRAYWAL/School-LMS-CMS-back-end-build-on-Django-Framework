from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import mimetypes
from django.utils import timezone

User = get_user_model()



def validate_file_type(file, content_type):
    """
    Validates the file type based on the content type.
    :param file: Uploaded file
    :param content_type: Type of the content (e.g., video, pdf, slide, etc.)
    :raises ValidationError: If the file type is not valid for the content type
    """
    # Define allowed MIME types for each content type
    allowed_mime_types = {
        'video': ['video/mp4', 'video/x-msvideo', 'video/x-matroska'],
        'pdf': ['application/pdf'],
        'slide': ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'],
        'interactive': ['application/zip', 'application/x-shockwave-flash'],
    }

    # Get the MIME type of the uploaded file
    mime_type, _ = mimetypes.guess_type(file.name)

    # Check if the content type has a restriction and validate it
    if content_type in allowed_mime_types:
        if mime_type not in allowed_mime_types[content_type]:
            raise ValidationError(f'Invalid file type for {content_type}. Allowed types are: {", ".join(allowed_mime_types[content_type])}')
    else:
        raise ValidationError(f'Unsupported content type: {content_type}')

    # If no specific content type validation is needed, you can skip this function
    # Example: for 'text', 'quiz', or 'link', we might not need file validation


class Content(models.Model):
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('text', 'Text'),
        ('slide', 'Slide'),
        ('quiz', 'Quiz'),
        ('link', 'Link'),
        ('interactive', 'Interactive'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    course = models.ForeignKey('courses.Course', related_name='contents', on_delete=models.CASCADE)
    unit = models.ForeignKey('courses.Unit', related_name='contents', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='course_content/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)
    tags = models.ManyToManyField('Tag', related_name='contents', blank=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Validate the file type based on the content type
        if self.file and self.content_type in ['video', 'pdf', 'slide', 'interactive']:
            validate_file_type(self.file, self.content_type)

        # Ensure either file or URL is provided based on content type
        if self.content_type in ['video', 'pdf', 'slide', 'interactive'] and not self.file:
            raise ValidationError('File is required for this content type.')
        if self.content_type in ['link'] and not self.url:
            raise ValidationError('URL is required for this content type.')

    def is_released(self):
        return not self.released_at or self.released_at <= timezone.now()

    is_released.boolean = True  # Display it as a boolean field in the admin

    def __str__(self):
        return f"{self.title} (v{self.version})"


class ContentVersion(models.Model):
    content = models.ForeignKey(Content, related_name='versions', on_delete=models.CASCADE)
    version_number = models.IntegerField()
    file = models.FileField(upload_to='content_versions/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content.title} (v{self.version_number})"

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('download', 'Download'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, related_name='interactions', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.interaction_type} {self.content.title} on {self.timestamp}"

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    course = models.ForeignKey('courses.Course', related_name='assignments', on_delete=models.CASCADE)
    unit = models.ForeignKey('courses.Unit', related_name='assignments', on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey('courses.Lesson', related_name='assignments', on_delete=models.CASCADE, null=True, blank=True)
    content = models.ForeignKey('content.Content', related_name='assignments', on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    file_submission = models.BooleanField(default=True)
    text_submission = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ContentAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, related_name='accesses', on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} accessed {self.content.title}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ContentAnalytics(models.Model):
    content = models.ForeignKey(Content, related_name='analytics', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='content_analytics', on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    last_viewed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.content.title} analytics"
