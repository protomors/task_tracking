from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.db.models import Q, F, Value, When, Case
from datetime import datetime
from django.contrib.auth.views import LoginView

from .models import Task, Comment
from .forms import TaskForm, CommentForm
from .mixins import RedirectAuthenticatedUserMixin


class TaskListView(ListView):
    model = Task
    template_name = 'taskapp/task_list.html'
    context_object_name = 'tasks_list'

    def get_queryset(self):
        queryset = Task.objects.all()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        search_query = self.request.GET.get('search')
        my_tasks = self.request.GET.get('my_tasks')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')


        if my_tasks:
            queryset = queryset.filter(user=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                queryset = queryset.filter(due_date__gte=start_date_obj)
            except ValueError:
                pass  # Ігноруємо помилку парсингу дати

        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                queryset = queryset.filter(deadline__lte=end_date_obj)
            except ValueError:
                pass  # Ігноруємо помилку парсингу дати

        queryset = queryset.annotate(
            # Додаємо поле для сортування: 1 для завдань без дати, 0 для решти
            no_deadline=Case(
                When(deadline__isnull=True, then=Value(1)),
                default=Value(0),
            )
        ).order_by('no_deadline', 'deadline')

        return queryset

class TaskDetailView(DetailView):
    model = Task
    template_name = 'taskapp/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.all()  # Передайте коментарі до контексту
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.instance
            new_comment.task = self.get_object()
            new_comment.user = request.user
            new_comment.save()
        return redirect(request.path_info)

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'taskapp/task_form.html'
    success_url = '/list/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm 
    template_name = 'taskapp/task_form.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'taskapp/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

class SignUpView(RedirectAuthenticatedUserMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class LoginView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = 'registration/login.html'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'taskapp/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task = Task.objects.get(pk=self.kwargs['task_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.kwargs['task_pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'taskapp/comment_update.html'

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'taskapp/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})
