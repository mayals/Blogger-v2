from .models import Category

def context_categories(request):
    categories = Category.objects.all()
    return {
        'con_categories': categories,
        }