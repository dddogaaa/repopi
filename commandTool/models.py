from django.db import models

class Result(models.Model):
    status = models.IntegerField()
    message = models.CharField(max_length=200)
    command = models.CharField(max_length=200)
    name = models.CharField(max_length=200,blank=True,null=True,default=None)
    execution_time = models.FloatField(blank=True, null=True)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    file = models.CharField(max_length=200, null=True, default=None, blank=True)