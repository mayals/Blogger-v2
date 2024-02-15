from .models import Category,Post

def context_categories(request):
    categories = Category.objects.all().order_by('-posts_count')[:6]
    return {
        'con_categories': categories,
        }
    
def context_topposts(request):
    topposts   = Post.objects.all().order_by('-views_count')[:5]
    # print(topposts)
    return {
        'con_topposts': topposts,
        }