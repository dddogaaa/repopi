from django.db import models

class CommandExecution(models.Model):
    command = models.CharField(max_length=255)
    status = models.IntegerField()
    log_file = models.CharField(max_length=255)
    start_execution = models.DateTimeField(auto_now_add=True)
    end_execution = models.DateTimeField(auto_now=True)
    duration = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_execution and self.end_execution:
            self.duration = (self.end_execution - self.start_execution).total_seconds()
        super().save(*args, **kwargs)