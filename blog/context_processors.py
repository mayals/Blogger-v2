from .models import Category

def context_categories(request):
    categories = Category.objects.all().order_by('-posts_count')
    return {
        'con_categories': categories,
        }