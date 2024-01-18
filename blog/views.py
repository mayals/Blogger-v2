from django.shortcuts import render
from .models import Post, Category


def posts_view(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    context ={
        'categories' : categories,
        'posts' : posts,    
    }
    return render(request,'blog/index.html', context)


