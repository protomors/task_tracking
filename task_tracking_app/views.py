from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'taskapp/task_list.html'
    context_object_name = 'tasks_list'
    login_url = 'login'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class TaskDetailView(DetailView):
    model = Task
    template_name = "taskapp/task_detail.html"
    context_object_name = "task"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'taskapp/task_form.html'
    success_url = '/list/'

    def form_valid(self, form):
        # Присвоюємо користувача, який створює завдання
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm 
    template_name = 'taskapp/task_form.html'

    def get_queryset(self):
        # Переконуємось, що можна редагувати тільки свої завдання
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # Присвоюємо користувача, який редагує завдання (хоча користувач вже не змінюється)
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'taskapp/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        # Переконуємось, що можна видаляти тільки свої завдання
        return Task.objects.filter(user=self.request.user)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
