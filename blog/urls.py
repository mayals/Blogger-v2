from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('new-post/', views.create_post, name='new-post')
    

]
