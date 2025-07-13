from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, AIDescriptionView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/ai/generate-description/', AIDescriptionView.as_view(), name='ai-generate-description'),
]
