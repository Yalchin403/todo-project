from __future__ import absolute_import, unicode_literals
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from .models import Task
from django.core.mail import send_mail
from todo.settings import EMAIL_HOST_USER


@shared_task
def send_emails():
    tasks = Task.objects.all()
    for task in tasks:

        email = task.owner.email
        subject = f"Your {task.title} task is not done yet"
        message = f"""
            Your {task.title} task is not done yet,
            this is kind reminder to make you aware that it's deadline is due {task.deadline}
            Don't forget to get it done!
            """
        send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently = False)
