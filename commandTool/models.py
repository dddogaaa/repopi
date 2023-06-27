from django.db import models

class Response(models.Model):
    status = models.IntegerField()
    message = models.CharField(max_length=200)
    command = models.CharField(max_length=200)
    execution_time = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    output_file = models.CharField(max_length=200, null=True, default=None)
