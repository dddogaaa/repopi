from django.urls import path,re_path
from .views import *


urlpatterns = [
    path('echo/', hello),
    path('getList/', getList),
    path('showPath/', showPath),
    path('longCmd/', longCmd),
    path('filter/', filter),
    path('list-outputs/', list_outputs),
    path('definitions/',definitions),
]