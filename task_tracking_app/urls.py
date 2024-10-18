from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskDeleteView, TaskUpdateView, SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("list/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("task/new", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
