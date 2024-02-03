from django import forms
from .models import Post,Comment
from django_ckeditor_5.widgets import CKEditor5Widget


class PostForm(forms.ModelForm):
    title   = forms.CharField(label='Title',
                              max_length=70,
                              required=True,
                              disabled=False,
                              widget  = forms.TextInput(attrs = {'class':'form-control',}),
                              )
   
   #  content = forms.CharField(widget=CKEditorWidget())
    
    
    widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
   
   
    # content = forms.CharField(label='Content',
    #                      min_length=10000,
    #                       help_text='the min length of this field is 10000',
    #                         widget = forms.Textarea(attrs={'rows': 5,
    #                                                       'class':'form-control',
    #                                                     'placeholder': 'write post .. '
    #                                                     }))

    
    
    # widgets = {
        #     "text": CKEditor5Widget(
        #         attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #     )
        # }
    
    class Meta:
            model   = Post
            fields  = ['title', 'content', 'category', 'tags','photo']
            
            
            
class CommentForm(forms.ModelForm):
    name     = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Name..'}))
    email    = forms.EmailField(label='',help_text='Email will be hidden', widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    message  = forms.CharField(label='', help_text='Please add comment related to the post',min_length='20', widget = forms.Textarea(attrs={'rows': 5, 
                                                                                                                            'class':'form-control',
                                                                                                                           'placeholder': 'Your Comment .. '}))
                                                                               
    class Meta:
        model   = Comment
        fields  = ['name', 'email', 'message']