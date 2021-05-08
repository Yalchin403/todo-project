from django.urls import path
from . import views


app_name = 'comments'
urlpatterns = [
    path('<str:task_id>/',views.CommentView.as_view(), name='comment'),

]