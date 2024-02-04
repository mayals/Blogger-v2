from django.contrib.sitemaps import Sitemap
from .models import Post,Category,Tag
from django.urls import reverse

class PostSitemap(Sitemap):
    # changefreq: Indicates how often pages are expected to change (always, hourly, daily, weekly, monthly, yearly, never).
    changefreq = "weekly"
    # priority: Indicates the relative importance of a page compared to others on your site (0.0 to 1.0).
    priority = 0.9
    
    def items(self):
        return Post.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
       # return reverse('post-detail', kwargs={'slug':obj.slug})  # Replace 'post-detail' with your actual URL pattern name
        return obj
    
    
    
    
class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Category.objects.filter(slug__isnull=False)  # Only include categories with slugs

    # Omitting lastmod: The lastmod method has been removed as it's not applicable without a field tracking the last modification date.
    # def lastmod(self, obj):
    #     return obj.updated_at

    
    
    
class TagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Tag.objects.filter(slug__isnull=False)  # Only include tags with slugs

    # Omitting lastmod: The lastmod method has been removed as it's not applicable without a field tracking the last modification date.
    # def lastmod(self, obj):
    #     return obj.updated_at