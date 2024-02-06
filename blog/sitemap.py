from django.contrib.sitemaps import Sitemap
from .models import Post,Category,Tag
from django.shortcuts import reverse


# https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/#sitemap-classes
class PostSitemap(Sitemap):
    # changefreq and priority are class attributes corresponding to <changefreq> and <priority> elements, respectively. They can be made callable as functions, as lastmod was in the example.
    # changefreq: Indicates how often pages are expected to change (always, hourly, daily, weekly, monthly, yearly, never).
    changefreq = "weekly"
    
    # priority: Indicates the relative importance of a page compared to others on your site (0.0 to 1.0).
    priority = 0.9
    
    # items() is a method that returns a sequence or QuerySet of objects. 
    # The objects returned will get passed to any callable methods corresponding to a sitemap property (location, lastmod, changefreq, and priority).
    def items(self):
        return Post.objects.filter(is_published=True)
    
    # lastmod should return a datetime.
    def lastmod(self, obj):
        return obj.updated_at
    
    # By default, location() calls get_absolute_url() on each object and returns the result.
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