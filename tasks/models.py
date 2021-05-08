from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings


class Task(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField(max_length = 2000)
    deadline = models.DateTimeField()
    done = models.BooleanField(default = False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    def __str__(self):
        return self.title

class Permission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'shared_users', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, related_name = 'shared_task', on_delete=models.CASCADE, null=True)
    mode = models.BooleanField(default = False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return self.task.title + "- shared with " + self.user.username