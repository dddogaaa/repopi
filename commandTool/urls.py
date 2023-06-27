# from django.urls import path
# from . import views

# urlpatterns = [
#     path('serve_log_file/', views.serve_log_file, name='serve_log_file'),
#     path('list_logs/', views.list_logs, name='list_logs'),
#     path('execute_command/', views.execute_command, name='execute_command'),
# ]

from django.urls import path
from .views import *
from django.urls import re_path


urlpatterns = [
    path('run-commands/', run_commands, name='run_commands'),
    path('filter-by-commands/', filter_by_commands, name='filter_by_commands'),
    re_path(r'^filter-by-commands/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),
    path('list-logs/', list_logs, name='list_logs'),
    path('filter-by-date/', filter_by_date, name='filter-by-date'),
    re_path(r'^filter-by-date/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),
    path('filter-by-status/', filter_by_status, name='filter_by_status'),
    re_path(r'^filter-by-status/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),
]