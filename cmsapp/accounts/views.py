from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import UserProfile
from assessments.models import  Assessment, Submission
from courses.models import Course 
from .serializers import CustomUserSerializer, UserProfileSerializer
from assessments.serializers import AssessmentSerializer, SubmissionSerializer
from courses.serializers import CourseSerializer
CustomUser = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'signup':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        request.data['is_student'] = True
        request.data['is_instructor'] = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user
        user_profile_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_student': user.is_student,
            'is_instructor': user.is_instructor,
        }

        if user.is_student:
            courses = Course.objects.filter(students=user)
            completed_assessments = Submission.objects.filter(student=user, status='completed')
            pending_assessments = Assessment.objects.filter(course__in=courses).exclude(submissions__student=user)
        else:
            courses = Course.objects.filter(instructor=user)
            completed_assessments = Assessment.objects.filter(course__in=courses, submissions__status='completed')
            pending_assessments = Assessment.objects.filter(course__in=courses).exclude(submissions__status='completed')

        user_profile_data['courses'] = CourseSerializer(courses, many=True).data
        user_profile_data['completed_assessments'] = SubmissionSerializer(completed_assessments, many=True).data
        user_profile_data['pending_assessments'] = AssessmentSerializer(pending_assessments, many=True).data

        return Response(user_profile_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def assign_course(self, request, pk=None):
        user = self.get_object()
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        user.courses.add(course)
        return Response({"detail": "Course assigned successfully"})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def remove_course(self, request, pk=None):
        user = self.get_object()
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        user.courses.remove(course)
        return Response({"detail": "Course removed successfully"})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def set_instructor_role(self, request, pk=None):
        user = self.get_object()
        user.is_instructor = True
        user.is_student = False
        user.save()
        return Response({"detail": "User set as instructor successfully"})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def set_student_role(self, request, pk=None):
        user = self.get_object()
        user.is_instructor = False
        user.is_student = True
        user.save()
        return Response({"detail": "User set as student successfully"})
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)