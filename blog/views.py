from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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



def post_create(request):
    form = PostForm()
    if request.method == 'POST' :
        form = PostForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request,f'Thanks ( {request.user.first_name} ), your post added successfully !')
            form = PostForm()
            return redirect('blog:home')
            
        else:
            form = PostForm(request.POST, request.FILES)
            messages.error(request,f'Post not add correctly! please complete those fields below.!')
    
    context = {
            'form': form,
    }
    return render(request,'blog/post_create.html',context)





def post_detail(request,slug):
    post = get_object_or_404(Post, slug= slug) 
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context= {
        'post' : post ,
        'categories' : categories,
        'tags'       : tags,
        
    }
    return render(request,'blog/post_detail.html',context)
