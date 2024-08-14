from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    EnrollmentListCreateView, EnrollmentDetailView,
    ProgressListCreateView, ProgressDetailView,
    CourseCompletionListCreateView, CourseCompletionDetailView,
    AttendanceListCreateView, AttendanceDetailView
)

urlpatterns = [
    # Enrollment URLs
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),

    # Progress URLs
    path('progresses/', ProgressListCreateView.as_view(), name='progress-list-create'),
    path('progresses/<int:pk>/', ProgressDetailView.as_view(), name='progress-detail'),

    # Course Completion URLs
    path('course-completions/', CourseCompletionListCreateView.as_view(), name='course-completion-list-create'),
    path('course-completions/<int:pk>/', CourseCompletionDetailView.as_view(), name='course-completion-detail'),

    # Attendance URLs
    path('attendances/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendances/<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),
]
