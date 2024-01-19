from django.shortcuts import render
from .models import Post, Category,Tag
from .forms import PostForm

def home_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.all()
    
    context ={
        'categories' : categories,
        'tags'       : tags,
        'posts'      : posts,    
    }
    return render(request,'blog/home.html', context)



def create_post(request):
    form = PostForm(request.POST)
    context:{
        'form':form,
    }
    return render(request,'blog/create_post.html',context)