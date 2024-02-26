from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cat/<slug:catslug>/', views.home_view, name='home-filter-category'),
    path('tag/<slug:tagslug>/', views.home_view, name='home-filter-tag'),
    # Post
    path('new-post/', views.post_create, name='new-post'),
    path('post-detail/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='post-detail'),
    path('post-update/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_update, name= 'post-update'),
    path('post-delete-confirm/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_delete_confirm, name ='post-delete-confirm'),
    path('post-like/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_like_action, name='post-like'),
    path('post-share-by-email/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_share_by_email, name='post-share-by-email'),
   
    path('google7a03622cb96e4f8f.html', views.google_verification_view),

    # Category
    path('categories/', views.categories, name='categories'),
    path('cat-detail/<slug:cat_slug>/', views.cat_detail, name='cat-detail'),

    # Tag
    path('tags/', views.tags, name='tags'),
    path('tag-detail/<slug:tag_slug>/', views.tag_detail, name='tag-detail'),
]
