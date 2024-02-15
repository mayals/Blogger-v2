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
        
class SharePostByEmailForm(forms.Form):
        sender_name     = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name..'}))
        sender_email    = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Email..'}))
        recipient_email = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Recipient Email..'}))
        sender_comment  = forms.CharField(label='', required=True, help_text='Please add comment related to the sharing the post', widget = forms.Textarea(attrs={'rows': 5, 'class':'form-control', 'placeholder': 'Your Comment ..'})) 
                                                                                                                                                  
        def clean_sender_name(self):
            sender_name = self.cleaned_data['sender_name']
            if len(sender_name) == 0 :
                raise forms.ValidationError('sender_name must not be empty.')
            return sender_name   
        
        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('sender_name') == "" or cleaned_data.get('sender_email') == "" or cleaned_data.get('recipient_email')  == "" :
                raise forms.ValidationError('Field not empty.')
            return cleaned_data                                                                                                                              