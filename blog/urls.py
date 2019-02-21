from django.urls import path
from . import views

urlpatterns = [
    # if you go to: 127.0.0.1:8000 you'll be redirected to:
    path('', views.post_list, name='post_list'),
]