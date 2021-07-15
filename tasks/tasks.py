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
from .models import Task
from django.dispatch import receiver
from django.db.models.signals import post_save


@shared_task
def send_emails(id):
    task = Task.objects.get(id=id)
    if not task.done :
        deadline = localtime(task.deadline)
        email = task.owner.email
        subject = f"Your {task.title} task is not done yet"
        message = f"""
            Your task named as - {task.title} is not done yet,
            this is kind reminder to make you aware that its deadline is due {task.deadline}.
            Don't forget to get it done asap!
            """
        send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently = False)

        
@receiver(post_save, sender=Task)
def remind_user(sender, instance, created, **kwargs):
    # print("Signals recieved.", instance, created, kwargs)
    if created:
        time_zone = pytz.timezone('Asia/Baku')
        now, DIFFERENCE = datetime.now(time_zone), 600
        REMINDER_TIME = (localtime(instance.deadline) - now).total_seconds() - DIFFERENCE
        print(REMINDER_TIME)
        send_emails.apply_async(args=[instance.id], countdown=REMINDER_TIME)
