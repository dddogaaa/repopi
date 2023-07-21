from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^jobs/output/(?P<djID>\d+)/?$', views.index, name='index'),
    re_path(r'^jobs/status/(?P<status>\d+)/?$', views.jobs_w_status),
    re_path(r'^jobs/(?P<id>\d+)/?$', views.jobs_w_id),
    path('jobs/', views.jobs),
    path('streaming/<int:djID>/', views.stream, name='stream'),
    path('stream2/', views.stream2),
    path('repo/echo/', views.hello),
    path('repo/getList/', views.getList),
    path('repo/showPath/', views.showPath),
    path('repo/longCmd/', views.longCmd),
]
