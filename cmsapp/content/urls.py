from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentViewSet, AssignmentViewSet, ContentVersionViewSet, InteractionViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'content', ContentViewSet, basename='content')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'content-versions', ContentVersionViewSet, basename='contentversion')
router.register(r'interactions', InteractionViewSet, basename='interaction')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    # Custom action paths
    path('content/<int:pk>/add-version/', ContentViewSet.as_view({'post': 'add_version'}), name='content-add-version'),
    path('content/<int:pk>/track-interaction/', ContentViewSet.as_view({'post': 'track_interaction'}), name='content-track-interaction'),
    path('content/search/', ContentViewSet.as_view({'get': 'search_content'}), name='content-search'),
    path('content/filter/', ContentViewSet.as_view({'get': 'filter_content'}), name='content-filter'),
    path('assignments/<int:pk>/submit/', AssignmentViewSet.as_view({'post': 'submit_assignment'}), name='assignment-submit'),
    path('assignments/by-course-and-unit/', AssignmentViewSet.as_view({'get': 'list_by_course_and_unit'}), name='assignment-by-course-and-unit'),
]
