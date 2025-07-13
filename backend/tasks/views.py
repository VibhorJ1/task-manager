from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .ai import generate_task_description
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        status_param = self.request.query_params.get('status')
        priority_param = self.request.query_params.get('priority')

        if status_param:
            now = timezone.now()
            if status_param == 'completed':
                queryset = queryset.filter(is_completed=True)
            elif status_param == 'upcoming':
                queryset = queryset.filter(is_completed=False, deadline__gt=now)
            elif status_param == 'missed':
                queryset = queryset.filter(is_completed=False, deadline__lte=now)

        if priority_param:
            queryset = queryset.filter(priority=priority_param.lower())

        return queryset


    @action(detail=False, methods=['get'])
    def status(self, request):
        grouped = Task.get_tasks_by_status()
        return Response({
            'upcoming': TaskSerializer(grouped['upcoming'], many=True).data,
            'completed': TaskSerializer(grouped['completed'], many=True).data,
            'missed': TaskSerializer(grouped['missed'], many=True).data,
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.is_completed:
            return Response({"detail": "Task is already completed."}, status=status.HTTP_400_BAD_REQUEST)

        task.mark_completed()
        return Response({"detail": "Task marked as completed successfully."}, status=status.HTTP_200_OK)


class AIDescriptionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        title = request.data.get("title", "").strip()
        if not title:
            raise ValidationError({"title": "This field is required."})

        try:
            description = generate_task_description(title)
            return Response({"description": description})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)