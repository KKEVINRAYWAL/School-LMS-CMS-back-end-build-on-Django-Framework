#courses/models.py
from django.db import models
from django.apps import apps
from accounts.models import CustomUser

class Semester(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.ForeignKey(CustomUser, related_name='instructed_courses', on_delete=models.CASCADE)  
    semester = models.ForeignKey(Semester, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Unit(models.Model):
    course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    required_for_completion = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Lesson(models.Model):
    unit = models.ForeignKey(Unit, related_name='lessons', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)  # Add this line
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    contents = models.ManyToManyField('content.Content', related_name='lessons', blank=True)

    def __str__(self):
        return self.title
class LessonPlan(models.Model):
    lesson = models.OneToOneField(Lesson, related_name='lesson_plan', on_delete=models.CASCADE)
    objectives = models.TextField()
    materials_needed = models.TextField(blank=True)
    lesson_procedure = models.TextField()
    assessment_methods = models.TextField()
    lesson_reflection = models.TextField(blank=True)

    def __str__(self):
        return f"Lesson Plan for {self.lesson.title}"

class StudyMaterial(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='study_materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, related_name='course_enrollments_courses', on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    course = models.ForeignKey(Course, related_name='course_enrollments_courses', on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"

class Progress(models.Model):
    student = models.ForeignKey(CustomUser, related_name='lesson_progresses_courses', on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    lesson = models.ForeignKey(Lesson, related_name='lesson_progresses_courses', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username}'s progress in {self.lesson.title}"
