from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.posts_view, name='index'),
    

]
