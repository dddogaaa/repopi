from django.db import models

class Response(models.Model):
    status = models.IntegerField()
    message = models.CharField(max_length=200)
    command = models.CharField(max_length=200)
    execution_time = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    output_file = models.CharField(max_length=200, null=True, default=None, blank=True)
    thread_ID = models.IntegerField(null=True, blank=True)
