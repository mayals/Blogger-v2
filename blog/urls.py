from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('new-post/', views.post_create, name='new-post'),
    path('post-detail/<slug:slug>/', views.post_detail, name='post-detail'),
    path('post-update/<slug:slug>/', views.post_update, name= 'post-update')
]
