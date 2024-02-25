from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Category,Tag
from .forms import PostForm, CommentForm, SharePostByEmailForm
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage


def home_view(request):
    categories = Category.objects.all().order_by('-posts_count')
    tags       = Tag.objects.all()
    posts      = Post.objects.all()
    
    if 'sc' in request.GET:    
       sc = request.GET['sc']
       posts = posts.filter(title__contains=sc) 
 
    context ={
        'categories' : categories,
        'tags'       : tags,
        'posts'      : posts,
       
    }
    return render(request,'blog/home.html', context)



def home_filter_category(request,catslug):
    categories = Category.objects.all().order_by('-posts_count')
    tags       = Tag.objects.all()
    posts      = Post.objects.all()
       
    if catslug != None:
       posts = posts.filter(category__slug=catslug)
      
    context ={
        'categories' : categories,
        'tags'       : tags,
        'posts'      : posts,    
    }
    return render(request,'blog/home.html', context)



def home_filter_tag(request,tagslug):
    categories = Category.objects.all().order_by('-posts_count')
    tags       = Tag.objects.all()
    posts = Post.objects.all()
    if tagslug :
        posts = posts.filter(tags__slug=tagslug)
    
             
    context ={
        'categories' : categories,
        'tags'       : tags,
        'posts'      : posts,    
    }
    return render(request,'blog/home.html', context)





@login_required(login_url='user:user-login')
def post_create(request):
    form = PostForm()
    if request.method == 'POST' :
        form = PostForm(request.POST, request.FILES)
      
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





def post_detail(request,year,month,day,post_slug):
    # Post
    post = get_object_or_404(Post,slug=post_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
                                    status=Post.Status.PUBLISHED
    ) 
    categories = Category.objects.all().order_by('-posts_count')
    tags = Tag.objects.all()
    
    # post_views_count
    # Get the session key for this post
    my_session_key = 'session_key_for_post_id_{}'.format(post.id)
    # print(my_session_key)
    # Check if the session key exists in the session
    if not request.session.get(my_session_key,False):
        # print("key not exist")
        # If the session key doesn't exist in request.session, increment views_count and set the session key
        post.views_count += 1
        post.save()
        request.session[my_session_key] = True
        # print(request.session[my_session_key])
    
    
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
           return redirect('blog:post-detail',year=year,month=month,day=day,post_slug=post_slug)        
        
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




@login_required(login_url='user:user-login')
def post_update(request,year,month,day,post_slug): 
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                                    slug=post_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    if post.author == request.user :
        form= PostForm(instance=post)
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES,instance=post)
            if form.is_valid():
                updated_post = form.save(commit=False)
                updated_post.author = request.user
                updated_post.save()
                form.save_m2m() 
                messages.success(request,f'Thanks ( {request.user.first_name} ), your post updated successfully !')
                return redirect('blog:post-detail',year=year,month=month,day=day,post_slug=post.slug)
            
            else:
                form = PostForm(request.POST,request.FILES,instance=post)
                messages.error(request,f'Post not update correctly! please complete those fields below.!')
             
    else:
        messages.warning(request,f"Sorry, you have no permission to update this post, only post's author can update it")
        return redirect('blog:home')
    
    context ={
        'post':post,
        'form' : form ,
    }
    return render(request,'blog/post_update.html',context)




@login_required(login_url='user:user-login')
def post_delete_confirm(request,year,month,day,post_slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                                    slug=post_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
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
    
    


@login_required(login_url='user:user-login')   
def post_like_action(request,year,month,day,post_slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                                    slug=post_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    
    if post.likes.filter(id=request.user.id).exists() == False :
        post.likes.add(request.user)
        
    else:
        post.likes.remove(request.user)
        
    # post_likes_count=liked_post.count()       
    return redirect('blog:post-detail',year=year,month=month,day=day,post_slug=post_slug)




def post_share_by_email(request,year,month,day,post_slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                                    slug=post_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    form = SharePostByEmailForm()
    if request.method == 'POST':
        form = SharePostByEmailForm(request.POST)
        # print("form"+ str(form))
        if form.is_valid():
            cd = form.cleaned_data
            print("cd="+ str(cd))
            sender_name = cd.get('sender_name')
            sender_email = cd.get('sender_email')
            recipient_email = cd.get('recipient_email')
            sender_comment = cd.get('sender_comment')
            
            # https://docs.djangoproject.com/en/4.2/topics/email/#send-mail
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)¶
            subject = f"{sender_name} recommends you read {post.title}"
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = f"Read {post.title} at {post_url} \n {sender_name}\'s comments:{sender_comment}"
            from_email =  sender_email
            recipient_list = [recipient_email]
            send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            print("send_mail=",send_mail(subject,message,from_email,recipient_list))
            messages.success(request,f'Thanks ( {sender_name} ), for sharing the post ({post.title}).')
            return redirect('blog:post-detail',year=year,month=month,day=day,post_slug=post_slug)
    
        else:
            form = SharePostByEmailForm()
            messages.error(request,f'The post ({post.title}) not shared! please try again')
            
    else:
        form = SharePostByEmailForm()
    
    context = {
        'post': post,
        'form': form,
    }
    return  render(request,'blog/post_share.html',context=context)    









#  https://search.google.com/search-console
def google_verification_view(request):
    return TemplateView.as_view(template_name='google7a03622cb96e4f8f.html')(request)


