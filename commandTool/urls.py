from django.urls import path,re_path
from . import views

urlpatterns = [
    # re_path(r'^jobs/output/(?P<djID>\d+)/?$', views.index, name='index'),
    path('index/',views.index),
    path('streaming/<int:djID>/', views.stream, name='stream'),
    path('jobs/', views.jobs),
    path('jobs_data/', views.jobs_data),
    re_path(r'^jobs/(?P<id>\d+)/?$', views.get_job),
    # re_path(r'^jobs/status/(?P<status>\d+)/?$', views.jobs_w_status),
    path('jobs/filter/',views.jobs_filter),
    path('repo/',views.repo),
    path('repo/hello/', views.hello),
    path('repo/getList/', views.getList),
    path('repo/showPath/', views.showPath),
    path('repo/longCmd/', views.longCmd),
    path('repo/wrong/',views.wrong),
    path('home/',views.base),
]
