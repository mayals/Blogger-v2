from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    title   = forms.CharField(label='Title',
                              max_length=70,
                              required=True,
                              disabled=False,
                              widget  = forms.TextInput(attrs = {'class':'form-control',}),
                              )
   
    content = forms.CharField(widget=CKEditorWidget())
   
   
    # content = forms.CharField(label='Content',
    #                      min_length=10000,
    #                       help_text='the min length of this field is 10000',
    #                         widget = forms.Textarea(attrs={'rows': 5,
    #                                                       'class':'form-control',
    #                                                     'placeholder': 'write post .. '
    #                                                     }))
    
    
    class Meta:
            model   = Post
            fields  = ['title', 'content', 'category', 'tags','photo']
            
            
            
