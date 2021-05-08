from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


# Create your views here.
class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:home')
        else:
            form = CreateUserForm()
            context = {'form': form}
            return render(request, "account/signup.html", context)
    def post(self, request):

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            user_obj = User.objects.get(username=user)
            user_obj.is_active = False
            user_obj.save()
            messages.success(request, f'{user}, account has been successfully created for you')
            return redirect('account:signIn')
        else:
            return render(request, 'account/signup.html', {'form':form})

class SignIn(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:home')
        return render(request, 'account/signin.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.get(username=username)
        user = authenticate(request, username=username, password=password)

        if user_obj.is_active:
            if user is not None:
                login(request, user)
                return redirect('tasks:home')
            
            else:
                messages.info(request, 'Email or password invalid')
                return render(request, 'account/signin.html')

        messages.error(request, "Your account is not active!")
        return render(request, 'account/signin.html')


class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect('account:signIn')
