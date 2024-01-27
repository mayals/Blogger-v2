from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from user.models import UserModel

# https://pypi.org/project/django-ckeditor/#installation 
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
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_user')
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts_category')
    tags         = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=True)          
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):    
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})
    
    @property
    def get_user(self):
        user = UserModel.objects.get(email=self.author)
        print('user=',user)
        return user 
        
    @property
    def get_post_category(self):
        return  self.category
        
    @property
    def get_post_tags(self):
        return self.tags
    
    class Meta:
        ordering            = ['-created_at']
        verbose_name        = 'Post'
        verbose_name_plural = 'Posts'
    
    
    
    
    
class Comment(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    post          = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    message       = models.TextField(blank=False)
    name          = models.CharField(max_length=50, null=True,blank=False)
    email         = models.EmailField(null=True, blank=False)
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default='p')
    created_at    = models.DateTimeField(null=True, auto_now_add=True, auto_now=False)
    published_at  = models.DateTimeField( auto_now_add=True, auto_now=False, null=True)
  
    def __str__(self):
        return 'Commented by ({}) on the post: "{}" '.format(self.name, self.post)
    class Meta:
        ordering = ('-published_at',)