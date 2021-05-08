from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.TaskList.as_view(), name = "home"),
    path('about', views.AboutView.as_view(), name = "about"),
    path('create', views.TaskCreate.as_view(), name = "create"),
    path('update/<str:pk>', views.TaskUpdate.as_view(), name = "update"),
    path('delete/<str:pk>', views.TaskDelete.as_view(), name = "delete"),
    path('delete-share/<str:pk>', views.SharedTaskDelete.as_view(), name = "delete-share"),
    path('share/<str:pk>', views.TaskShare.as_view(), name = "share"),
    path('sharedwithme', views.SharedWith.as_view(), name = "sharedwithme"),
]
