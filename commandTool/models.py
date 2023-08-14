from django.db import models
from django.conf import settings as Settings

class Repo(models.Model):
    mirrorName = models.CharField(max_length=200,default=None,null=True)
    mirrorType = models.CharField(max_length=200,default=None,null=True)
    archiveUrl = models.URLField(default='https://depo.pardus.org.tr/pardus/')  
    dist = models.CharField(max_length=200, default=None,null=True)
    components = models.CharField(max_length=200, default=None,null=True)
    architectures = models.CharField(max_length=50, default=None,null=True)


class Result(models.Model):
    status = models.IntegerField()
    name = models.CharField(max_length=200,default=None)
    command = models.CharField(max_length=200, default=None)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    file = models.CharField(max_length=500, null=True, default=None, blank=True)

