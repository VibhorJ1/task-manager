from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    time_until_deadline = serializers.SerializerMethodField()
    days_until_deadline = serializers.IntegerField(read_only=True)
    hours_until_deadline = serializers.FloatField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def get_time_until_deadline(self, obj):
        return str(obj.time_until_deadline)
