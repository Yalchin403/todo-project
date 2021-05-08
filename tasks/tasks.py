from __future__ import absolute_import, unicode_literals
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from .models import Task
from django.core.mail import send_mail
from todo.settings import EMAIL_HOST_USER
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.utils.timezone import localtime
import pytz
from datetime import datetime


@shared_task
def send_emails():
    tasks = Task.objects.all()
    for task in tasks:
        
        time_zone = pytz.timezone('Asia/Baku')
        now = datetime.now(time_zone)
        deadline = localtime(task.deadline)
        diff = ((deadline - now).total_seconds())/60
        if 0<=diff<=10 and not task.done and not task.is_notified:
            email = task.owner.email
            subject = f"Your {task.title} task is not done yet"
            message = f"""
                Your task named as - {task.title} is not done yet,
                this is kind reminder to make you aware that its deadline is due {task.deadline}.
                Don't forget to get it done asap!
                """
            send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently = False)
            task.is_notified = True
            task.save()
