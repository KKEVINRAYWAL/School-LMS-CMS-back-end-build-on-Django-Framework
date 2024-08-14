from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from dateutil.parser import parse
from .models import Assessment, Submission
from .serializers import AssessmentSerializer, SubmissionSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    @action(detail=True, methods=['post'], url_path='extend-due-date')
    def extend_due_date(self, request, pk=None):
        assessment = self.get_object()
        new_due_date_str = request.data.get('new_due_date')

        try:
            new_due_date = parse(new_due_date_str)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        if new_due_date and timezone.now() < new_due_date:
            assessment.due_date = new_due_date
            assessment.save()
            return Response({'status': 'due date extended'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='by-course')
    def list_by_course(self, request):
        course_id = request.query_params.get('course_id')
        if course_id:
            assessments = self.queryset.filter(course_id=course_id)
            serializer = self.get_serializer(assessments, many=True)
            return Response(serializer.data)
        return Response({'error': 'Course ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='active-assessments')
    def active_assessments(self, request):
        student_id = request.user.id
        active_assessments = self.queryset.filter(course__enrollment__student_id=student_id, due_date__gte=timezone.now())
        serializer = self.get_serializer(active_assessments, many=True)
        return Response(serializer.data)

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=True, methods=['post'], url_path='submit')
    def submit_work(self, request, pk=None):
        assessment = get_object_or_404(Assessment, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user, assessment=assessment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='by-student')
    def list_by_student(self, request):
        student_id = request.query_params.get('student_id')
        if student_id:
            submissions = self.queryset.filter(student_id=student_id)
            serializer = self.get_serializer(submissions, many=True)
            return Response(serializer.data)
        return Response({'error': 'Student ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='grade')
    def grade_submission(self, request, pk=None):
        submission = self.get_object()
        grade = request.data.get('grade')

        try:
            grade = float(grade)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid grade'}, status=status.HTTP_400_BAD_REQUEST)

        if 0 <= grade <= submission.assessment.max_score:
            submission.grade = grade
            submission.save()
            return Response({'status': 'submission graded'}, status=status.HTTP_200_OK)
        return Response({'error': 'Grade must be between 0 and the maximum score'}, status=status.HTTP_400_BAD_REQUEST)

# Separate views for non-API endpoints
def index(request):
    assessments = Assessment.objects.all()
    context = {
        'assessments': assessments,
        'current_year': timezone.now().year
    }
    return render(request, 'assessments/index.html', context)

def detail(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    return render(request, 'assessments/detail.html', {'assessment': assessment})
