from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, Comment
from .forms import TaskForm, CommentForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment: Comment = comment_form.instance
            new_comment.task = self.get_object()
            new_comment.user = request.user
            new_comment.save()
        return redirect(request.path_info)

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "taskapp/comment_update.html"
    form_class = CommentForm

    def get_queryset(self):
        # Переконуємось, що можна редагувати тільки свої завдання
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        url = reverse_lazy('task-detail', kwargs={"pk": self.get_object().task.pk})
        return url
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'taskapp/comment_delete.html'
    form_class = CommentForm
    
    def get_queryset(self):
        # Переконуємось, що можна редагувати тільки свої завдання
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        url = reverse_lazy('task-detail', kwargs={"pk": self.get_object().task.pk})
        return url

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
    
    success_url = reverse_lazy('task-list')

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
