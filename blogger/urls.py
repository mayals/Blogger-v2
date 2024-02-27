from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# sitemaps
from django.contrib.sitemaps import GenericSitemap  # new
from django.contrib.sitemaps.views import sitemap  # new
from blog.sitemap import StaticSitemap, PostSitemap, CategorySitemap, TagSitemap 
from django.views.generic import TemplateView


sitemaps = {
   'static': StaticSitemap,
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
}


urlpatterns = [
   # https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/#module-django.contrib.sitemaps
   path("sitemap.xml/", sitemap, {"sitemaps":sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
   
   # robots.txt
   path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
   
   # google-site-verification
   #  https://search.google.com/search-console
   path('google-site-verification', TemplateView.as_view(template_name="google7a03622cb96e4f8f.html")),
   
   
   path('admin/', admin.site.urls),
   path('user/', include('user.urls', namespace='user')),
   path('', include('blog.urls', namespace='blog')),
   path('pages/', include('pages.urls', namespace='pages')),
    
    
   # https://pypi.org/project/django-ckeditor/#installation
   # path('ckeditor/', include('ckeditor_uploader.urls')),
   
   # https://pypi.org/project/django-ckeditor-5/
   path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
   
   
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)