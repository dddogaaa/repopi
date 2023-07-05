from django.urls import path
from .views import *
from django.urls import re_path


urlpatterns = [
    path('run-commands/', run_commands, name='run_commands'),
    path('filter-by-commands/', filter_by_commands, name='filter_by_commands'),
    re_path(r'^filter-by-commands/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),
    path('list-outputs/', list_outputs, name='list_outputs'),
    path('filter-by-date/', filter_by_date, name='filter-by-date'),
    re_path(r'^filter-by-date/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),
    path('filter-by-status/', filter_by_status, name='filter_by_status'),
    re_path(r'^filter-by-status/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),

]