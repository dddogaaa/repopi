from django.urls import path
from . import views

urlpatterns = [
    path('execute_command/', views.execute_command, name='execute_command'),
    path('<path:log_file_name>/', views.serve_log_file, name='serve_log_file'),
    path('logs_list', views.list_logs,name='list_logs'),
]