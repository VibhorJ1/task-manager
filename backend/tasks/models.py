from django.db import models

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Task(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
    )

    class Meta:
        ordering = ['deadline', '-priority']
        indexes = [
            models.Index(fields=['deadline']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} (Due: {self.deadline.strftime('%Y-%m-%d %H:%M')})"

    def clean(self):
        super().clean()

        if not self.pk and self.deadline <= timezone.now():
            raise ValidationError({
                'deadline': 'Deadline cannot be in the past for new tasks.'
            })

        if not self.title.strip():
            raise ValidationError({
                'title': 'Title cannot be empty.'
            })

    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()

        elif not self.is_completed and self.completed_at:
            self.completed_at = None

        super().save(*args, **kwargs)

    @property
    def status(self):
        if self.is_completed:
            return 'completed'

        if self.deadline <= timezone.now():
            return 'missed'

        return 'upcoming'

    @property
    def is_overdue(self):
        return not self.is_completed and self.deadline <= timezone.now()

    @property
    def time_until_deadline(self):
        return self.deadline - timezone.now()

    @property
    def days_until_deadline(self):
        return self.time_until_deadline.days

    @property
    def hours_until_deadline(self):
        return self.time_until_deadline.total_seconds() / 3600

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        self.is_completed = False
        self.completed_at = None
        self.save()

    @classmethod
    def get_upcoming_tasks(cls):
        return cls.objects.filter(
            is_completed=False,
            deadline__gt=timezone.now()
        ).order_by('deadline')

    @classmethod
    def get_completed_tasks(cls):
        return cls.objects.filter(is_completed=True).order_by('-completed_at')

    @classmethod
    def get_missed_tasks(cls):
        return cls.objects.filter(
            is_completed=False,
            deadline__lte=timezone.now()
        ).order_by('deadline')

    @classmethod
    def get_tasks_by_status(cls):
        return {
            'upcoming': cls.get_upcoming_tasks(),
            'completed': cls.get_completed_tasks(),
            'missed': cls.get_missed_tasks()
        }