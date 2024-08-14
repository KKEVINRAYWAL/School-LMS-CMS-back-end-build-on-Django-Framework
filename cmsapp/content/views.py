from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q  # Import Q for complex queries
from .models import Content, Assignment, ContentVersion, Interaction
from .serializers import ContentSerializer, AssignmentSerializer, ContentVersionSerializer, InteractionSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @action(detail=True, methods=['post'], url_path='add-version')
    def add_version(self, request, pk=None):
        content = self.get_object()
        serializer = ContentVersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content=content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='track-interaction')
    def track_interaction(self, request, pk=None):
        content = self.get_object()
        interaction_type = request.data.get('interaction_type')
        interaction = Interaction.objects.create(user=request.user, content=content, interaction_type=interaction_type)
        return Response({'status': 'interaction tracked'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search_content(self, request):
        query = request.query_params.get('q')
        if query:
            content = self.queryset.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query))
            serializer = self.get_serializer(content, many=True)
            return Response(serializer.data)
        return Response({'error': 'Query not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='filter')
    def filter_content(self, request):
        course_id = request.query_params.get('course_id')
        unit_id = request.query_params.get('unit_id')
        content = self.queryset.all()
        if course_id:
            content = content.filter(course_id=course_id)
        if unit_id:
            content = content.filter(unit_id=unit_id)
        serializer = self.get_serializer(content, many=True)
        return Response(serializer.data)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    @action(detail=True, methods=['post'], url_path='submit')
    def submit_assignment(self, request, pk=None):
        assignment = self.get_object()
        # Logic for submission would go here, such as saving files or handling text-based submissions
        return Response({'status': 'assignment submitted'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='by-course-and-unit')
    def list_by_course_and_unit(self, request):
        course_id = request.query_params.get('course_id')
        unit_id = request.query_params.get('unit_id')
        assignments = self.queryset.all()
        if course_id:
            assignments = assignments.filter(course_id=course_id)
        if unit_id:
            assignments = assignments.filter(unit_id=unit_id)
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)

class ContentVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentVersion.objects.all()
    serializer_class = ContentVersionSerializer

class InteractionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
