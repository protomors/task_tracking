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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"


# Для ролей та дозволів (наприклад, групи або права доступу можна додати через admin або middleware)
