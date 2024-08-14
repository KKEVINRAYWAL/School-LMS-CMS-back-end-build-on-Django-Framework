from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, SubmissionViewSet, index, detail

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'submissions', SubmissionViewSet, basename='submission')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs for the API endpoints
    path('index/', index, name='assessment_index'),  # Non-API endpoint for assessment index
    path('detail/<int:id>/', detail, name='assessment_detail'),  # Non-API endpoint for assessment detail
]
