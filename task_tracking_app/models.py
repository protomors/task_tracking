from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Модель для завдань
class Task(models.Model):
    # Вибір статусу
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    # Вибір пріоритету
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(auto_now_add=True, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.FileField(upload_to="task_media/", blank=True, null=True)
    

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("edit_task", "Can edit task"),  # Кастомний дозвіл на редагування
        ]



# Модель для коментарів до завдань
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task}"

