from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    icon = models.ImageField(verbose_name='Category Icon', default="img/cat_default.png", upload_to="blog/cat_img/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name






class Post(models.Model):
    id           = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(max_length=120, blank=True, null=True)
    content      = RichTextField()
    photo        = models.ImageField(verbose_name='Post Image', upload_to='blog/post-img/%Y/%m/%d/', null=True, blank=True)
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_author')
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts_category')
    tags         = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=True)          
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
    