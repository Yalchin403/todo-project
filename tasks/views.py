from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from tasks.owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.http import HttpResponse


class TaskList(OwnerListView):
    model = Task
    field = '__all__'
    success_url = reverse_lazy('tasks:home')
class TaskCreate(OwnerCreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:home')

class TaskUpdate(OwnerUpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:home')

class TaskDelete(OwnerDeleteView):
    model = Task
    template_name = 'tasks/confirm.html'
    success_url = reverse_lazy('tasks:home')

class AboutView(TemplateView):
    template_name = 'about.html'

class TaskShare(View):
    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        shared = Permission.objects.filter(owner = self.request.user)   # query set permissions
            
        content = {'task': task, 'shared': shared}
        return render(request, 'tasks/confirm_share.html', content)
    def post(self, request, pk):
        username = request.POST.get('username')
        mode = request.POST.get('mode')
        sharedUsername = User.objects.get(username = username)
        task = Task.objects.get(id = pk)
        is_exist = Permission.objects.filter(task=task, user=sharedUsername)
        if is_exist:
            return HttpResponse("This task is already shared with specified user!")
        
        permission = Permission(owner = self.request.user, user=sharedUsername, task=task)
        permission.save()
        if mode == "Yes":
            permission.mode = True
        else:
            permission.mode = False
        permission.save()
        return redirect('tasks:home')

class SharedTaskDelete(OwnerDeleteView):
    def get(self, request, pk):
        permission = Permission.objects.get(id = pk)
        content = {"permission": permission}
        return render(request, 'tasks/deleteshareconfirm.html', content)
    def post(self, request, pk):
        shared = Permission.objects.get(id = pk)
        if shared.owner == self.request.user or shared.user.all()[0] == self.request.user:
            shared.delete()
            return redirect('tasks:home')
        else:
            return HttpResponse("Trying to be hacker? Not even try bruh?")


class SharedWith(View):
    def get(self, request):
        shared_tasks = Permission.objects.filter(user = self.request.user)
        context = {"permissions": shared_tasks}
        return render(request, "tasks/shared_list.html", context)