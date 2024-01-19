from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    model: Post
    fields : '__all__'