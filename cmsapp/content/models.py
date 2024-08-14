from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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

    def __str__(self):
        return f"{self.title} (v{self.version})"

    def is_released(self):
        from django.utils import timezone
        return not self.released_at or self.released_at <= timezone.now()

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
    content = models.ForeignKey('content.Content', related_name='assignments', on_delete=models.CASCADE)  # Add this line
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
