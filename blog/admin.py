from django.contrib import admin
from .models import Category, Tag, Post, Comment

admin.site.register(Category)
admin.site.register(Tag)
#admin.site.register(Post)
admin.site.register(Comment)





#@admin.register(Post)   # another way to register Post 
class PostAdmin(admin.ModelAdmin):

    list_display = ['title','slug','author','category','status','published_at','views_count']
    list_filter = ['title','slug','author','category','status','published_at','views_count']
    search_fields = ['title', 'content']
    # prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    ordering = ['views_count', 'published_at']
    
    
admin.site.register(Post,PostAdmin)
    
   
    
    