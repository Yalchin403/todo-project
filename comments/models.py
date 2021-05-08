from django.db import models
from django.conf import settings
from tasks.models import Task

class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete = models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False)

    def __str__(self):

        return f"{self.task.title}-{self.owner.username}"