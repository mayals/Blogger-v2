from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# sitemaps
from django.contrib.sitemaps import GenericSitemap  # new
from django.contrib.sitemaps.views import sitemap  # new
from blog.sitemap import PostSitemap, CategorySitemap, TagSitemap 

sitemaps = {
    'posts': PostSitemap,
    #'categories': CategorySitemap,
    #'tags': TagSitemap,
}


urlpatterns = [
   path('admin/', admin.site.urls),
   path('user/', include('user.urls')),
   path('', include('blog.urls')),
   path('pages/', include('pages.urls')),
   
   # https://pypi.org/project/django-ckeditor/#installation
   # path('ckeditor/', include('ckeditor_uploader.urls')),
   
   # https://pypi.org/project/django-ckeditor-5/
   path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
   
   # https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/#module-django.contrib.sitemaps
   path("sitemap.xml", sitemap, {"sitemaps":sitemaps}, name="django.contrib.sitemaps.views.sitemap")

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)