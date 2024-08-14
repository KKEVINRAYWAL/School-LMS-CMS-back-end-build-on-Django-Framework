from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from courses.models import Course, Unit, LessonPlan, StudyMaterial
from accounts.models import CustomUser

class Assessment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, related_name='assessments', on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name='assessments', null=True, blank=True, on_delete=models.SET_NULL)
    lesson_plan = models.ForeignKey(LessonPlan, related_name='assessments', null=True, blank=True, on_delete=models.SET_NULL)
    max_score = models.FloatField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    average_score = models.FloatField(null=True, blank=True, editable=False)
    completion_rate = models.FloatField(null=True, blank=True, editable=False)
    study_materials = models.ManyToManyField(StudyMaterial, related_name='assessments', blank=True)
    
    def clean(self):
        if self.max_score <= 0:
            raise ValidationError('Max score must be a positive number.')
        if self.due_date <= timezone.now():
            raise ValidationError('Due date must be in the future.')

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is called
        # Update average_score and completion_rate
        submissions = self.submissions.all()
        if submissions.exists():
            self.average_score = submissions.aggregate(models.Avg('grade'))['grade__avg']
            self.completion_rate = (submissions.filter(grade__isnull=False).count() / submissions.count()) * 100
        else:
            self.average_score = None
            self.completion_rate = None
        super().save(*args, **kwargs)

class Submission(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, related_name='submissions', on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    submitted_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)  # Added feedback field
    
    def __str__(self):
        return f"Submission by {self.student.username} for {self.assessment.name}"
