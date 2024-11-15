from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("list/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("task/new", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('comment/<int:task_pk>/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:task_pk>/update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
]
