from django.db import models
from django.conf import settings
from django.urls import reverse
from user.models import UserModel
from django.utils import timezone
from django.utils.text import slugify


# https://pypi.org/project/django-ckeditor/#installation 
# from ckeditor.fields import RichTextField

# https://pypi.org/project/shortuuid/
from shortuuid.django_fields import ShortUUIDField 

# https://pypi.org/project/django-ckeditor-5/
from django_ckeditor_5.fields import CKEditor5Field

# https://pypi.org/project/django-resized/
from django_resized import ResizedImageField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    icon = models.ImageField(verbose_name='Category Icon', default="img/cat_default.png", upload_to="blog/cat_img/%Y/%m/%d/", blank=True, null=True)
    posts_count = models.PositiveIntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        
        posts_count = Post.objects.filter(category=self).count()
        self.posts_count = posts_count
        super().save(*args, **kwargs)
    
    
    def get_category_posts(self):
        posts = Post.objects.filter(category=self)
        return posts  
    
    def get_absolute_url(self):
        return reverse("blog:cat-detail", args=[str(self.slug)])
         
    


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_tag_posts(self):
        posts = Post.objects.filter(tags=self)
        return posts

    def get_absolute_url(self):
        return reverse("blog:tag-detail", args=[str(self.slug)])


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT     = 'DR' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
         
    id           = ShortUUIDField(primary_key=True, unique=True, length=6, max_length=6, editable=False)
    title        = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=120, blank=True, null=True)
    content      = CKEditor5Field('Text', config_name='extends')
    # photo        = models.ImageField(verbose_name='Post Image', upload_to='blog/post-img/%Y/%m/%d/', null=True, blank=True)
    photo        = ResizedImageField(size=[600, 600], quality=85,verbose_name='Post Image', upload_to='blog/post-img/%Y/%m/%d/', null=True, blank=True)
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts_user')
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts_category')
    tags         = models.ManyToManyField(Tag)
    views_count  = models.PositiveIntegerField(default=0, blank=True)
    likes        = models.ManyToManyField(UserModel, related_name='post_users', blank=True)
    published_at = models.DateTimeField(default=timezone.now)        
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    status       = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
               

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):    
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        # return reverse("blog:post-detail", args=[str(self.slug)])
         return reverse("blog:post-detail", kwargs={"post_slug": self.slug,
                                                    "year": self.published_at.year,
                                                    "month":self.published_at.month,
                                                    "day":self.published_at.day})
        # return reverse("blog:post-detail", args=[str(self.slug)])
    
    @property
    def get_user(self):
        user = UserModel.objects.get(email=self.author)
        #print('user=',user)
        return user 
         
    @property
    def get_post_tags(self):
        return self.tags.all()
    
    @property
    def get_post_likes_count(self):
        return self.likes.all().count()
    
    class Meta:
        ordering = ('-published_at',)
        verbose_name        = 'Post'
        verbose_name_plural = 'Posts'
        unique_together=['title','published_at']
    
    
    
    
    
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
    published_at  = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
  
    def __str__(self):
        return 'Commented by ({}) on the post: "{}" '.format(self.name, self.post)
    class Meta:
        ordering = ('-published_at',)