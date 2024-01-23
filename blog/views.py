from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Category,Tag
from .forms import PostForm, CommentForm


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


@login_required()
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
    # Post
    post = get_object_or_404(Post, slug= slug) 
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # CommentForm
    form = CommentForm()
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid():
           new_comment = form.save(commit=False)
           new_comment.post = post
           new_comment.save()
           name = form.cleaned_data.get('name')
           messages.success(request,f'Thanks {name} , your comment added successfully !')
           form = CommentForm()
           return redirect('blog:post-detail',slug=post.slug)        
        
        else:
            messages.error(request,f'comment not add correctly, try again!')
    
    else:
        form = CommentForm()
    
    context= {
        'post'       : post ,
        'categories' : categories,
        'tags'       : tags, 
        'form'       : form, 
    }
    return render(request,'blog/post_detail.html',context)




@login_required()
def post_update(request,slug): 
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user :
        form= PostForm(instance=post)
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES,instance=post)
            print(form) 
            if form.is_valid():
                updated_post = form.save(commit = False)
                updated_post.author = request.user
                updated_post.save()
                form.save_m2m() 
                messages.success(request,f'Thanks ( {request.user.first_name} ), your post updated successfully !')
                return redirect('blog:home')
            
            else:
                form = PostForm(request.POST,request.FILES,instance=post)
                messages.error(request,f'Post not update correctly! please complete those fields below.!')
             
    else:
        messages.warning(request,f"Sorry, you have no permission to update this post, only post's author can update it")
        return redirect('blog:home')
    
    context ={
        'form' : form ,
    }
    return render(request,'blog/post_update.html',context)




@login_required()
def post_delete_confirm(request,slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user :
        if request.method == 'POST' and 'yes-delete'in request.POST:
            post.delete()
            messages.success(request,f'Thanks ( {request.user.first_name} ), your post deleted successfully !')
            return redirect('blog:home')
                
        context ={
            'post' : post ,
        }
        return render(request,'blog/post_delete_confirm.html',context)

        
    else:
        messages.warning(request,f"Sorry, you have no permission to delete this post, only post's author can delete it")
        return redirect('blog:home')
    