from django.shortcuts import render
from .models import Post, Category,Tag


def posts_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.all()
    
    context ={
        'categories' : categories,
        'tags'       : tags,
        'posts'      : posts,    
    }
    return render(request,'blog/index.html', context)