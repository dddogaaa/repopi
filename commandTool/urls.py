from django.urls import path
from . import views

urlpatterns = [
    path('serve_log_file/', views.serve_log_file, name='serve_log_file'),
    path('list_logs/', views.list_logs, name='list_logs'),
    path('execute_command/', views.execute_command, name='execute_command'),
]

