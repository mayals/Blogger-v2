from .models import Category,Post
from django.db.models import Count


# All Categories order by posts count
def context_categories(request):
    categories = Category.objects.all().order_by('-posts_count')[:6]
    return {
        'con_categories': categories,
        }
    
# All published Posts order by views count    
def context_topposts(request):
    topposts   = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-views_count')[:5]
    # print(topposts)
    return {
        'con_topposts': topposts,
        }
    
# All published Posts order by comments count    
def context_topcomments_posts(request):
    topcomments_posts  = Post.objects.filter(status=Post.Status.PUBLISHED).annotate(total_comments=Count('comments')).order_by('-total_comments')[:5]
    print(topcomments_posts)
    return {
        'con_topcomments_posts': topcomments_posts,
        }