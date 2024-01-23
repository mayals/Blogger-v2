from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('user-register/', views.user_create, name='user-register'),
]
