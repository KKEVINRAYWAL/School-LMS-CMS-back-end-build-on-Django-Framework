from rest_framework import viewsets, permissions
from .models import Course, Unit, Lesson, LessonPlan, StudyMaterial, Enrollment, Progress
from .serializers import CourseSerializer, UnitSerializer, LessonSerializer, LessonPlanSerializer, StudyMaterialSerializer, EnrollmentSerializer, ProgressSerializer
# Optionally, add additional actions to handle specific features like reporting, analytics, and role-based access control
from django.utils import timezone
# Example: Additional endpoint for generating reports
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg  # Import the Avg function

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonPlanViewSet(viewsets.ModelViewSet):
    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudyMaterialViewSet(viewsets.ModelViewSet):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.validated_data.get('completed'):
            serializer.save(date_completed=timezone.now())
        else:
            serializer.save()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        course = self.get_object()
        progress_data = Progress.objects.filter(lesson__unit__course=course)
        # Generate report based on progress data
        report = {
            'course': course.name,
            'total_students': course.enrollments.count(),
            'average_progress': progress_data.aggregate(Avg('completed')),
            'completion_rate': progress_data.filter(completed=True).count() / progress_data.count() if progress_data.exists() else 0,
        }
        return Response(report)

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

