
#enrollments/models.py
from django.db import models
from accounts.models import CustomUser
from courses.models import Course, Lesson
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, related_name='student_enrollments_enrollments', on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    course = models.ForeignKey(Course, related_name='course_enrollments_enrollments', on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed'), ('dropped', 'Dropped')], default='active')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"


class Progress(models.Model):
    student = models.ForeignKey(CustomUser, related_name='student_progresses_enrollments', on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    lesson = models.ForeignKey(Lesson, related_name='lesson_progresses_enrollments', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username}'s progress in {self.lesson.title}"

class CourseCompletion(models.Model):
    student = models.ForeignKey(CustomUser, related_name='student_course_completions', on_delete=models.CASCADE, limit_choices_to={'is_student': True})  # Change this line
    course = models.ForeignKey(Course, related_name='course_completions', on_delete=models.CASCADE)
    completion_date = models.DateField(auto_now_add=True)
    final_grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} completed {self.course.name} with grade {self.final_grade}"
class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, related_name='student_attendances', on_delete=models.CASCADE, limit_choices_to={'is_student': True})  # Change this line
    lesson = models.ForeignKey(Lesson, related_name='lesson_attendances', on_delete=models.CASCADE)  # Change this line
    attended_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent')], default='present')

    def __str__(self):
        return f"{self.student.username} - {self.status} for {self.lesson.title} on {self.attended_on.date()}"
