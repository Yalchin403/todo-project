# Generated by Django 3.1.4 on 2021-07-14 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_is_notified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_notified',
        ),
    ]