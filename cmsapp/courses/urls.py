from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, UnitViewSet, LessonViewSet, LessonPlanViewSet,
    StudyMaterialViewSet, EnrollmentViewSet, ProgressViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'units', UnitViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'lesson-plans', LessonPlanViewSet)
router.register(r'study-materials', StudyMaterialViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', ProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
