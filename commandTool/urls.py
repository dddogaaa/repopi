from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^jobs/output/(?P<djID>\d+)/?$', views.index, name='index'),
    path('streaming/<int:djID>/', views.stream, name='stream'),
    path('jobs/', views.jobs),
    re_path(r'^jobs/(?P<id>\d+)/?$', views.get_job),
    path('repo/echo/', views.hello),
    path('repo/getList/', views.getList),
    path('repo/showPath/', views.showPath),
    path('repo/longCmd/', views.longCmd),
]
