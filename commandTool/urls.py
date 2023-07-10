from django.urls import path,re_path
from .views import *


urlpatterns = [
    path('run/', runCommand, name='run-command'),
    path('filter-commands/', filter_commands, name='filter-commands'),
    re_path(r'^filter-commands/(?P<command_id>\d+)/?$', get_output_by_id, name='get_output_by_id'),
    path('list-outputs/', list_outputs, name='list_outputs'),
]