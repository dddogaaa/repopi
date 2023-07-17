from django.urls import path,re_path
from .views import *


urlpatterns = [
    path('echo/', hello),
    path('getList/', getList),
    path('showPath/', showPath),
    path('longCmd/', longCmd),
    path('filter-commands/', filter_commands),
    re_path(r'^filter-commands/(?P<command_id>\d+)/?$', get_output_by_id),
    path('list-outputs/', list_outputs),
    path('definitions/',definitions)
]