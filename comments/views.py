from django.shortcuts import render
from django.views import View
from .models import Comment
from tasks.models import Task, Permission
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

class CommentView(View):
    def get(self, request, task_id:str):
        # we have task_id
        # we have user_id
        # we can check permission
        task = Task.objects.get(id=task_id)
        user = request.user
        has_permission = Permission.objects.filter(task=task, user=user).first()
        is_owner = task.owner == user
        if has_permission:
            if has_permission.mode:
                content = self.handle_comments(task_id)
                return render(request, 'comments/detailView_comments.html', content)

            else:
                return HttpResponse("This task is shared with you, but permission for seeing comment section is not given")
        else:
            if is_owner:
                content = self.handle_comments(task_id)
                return render(request, 'comments/detailView_comments.html', content)
        return HttpResponse("You do not have any permission to see this task or its comment section!")

    @staticmethod
    def handle_comments(task_id):
        qs = Comment.objects.filter(task=task_id).order_by('updated_time')
        task_obj = get_object_or_404(Task, pk=task_id)
        content = {
            "task_obj": task_obj,
            "task_id": task_id,
            "comments": qs,
        }
        return content
    