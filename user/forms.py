from django import forms 
from .models import UserModel

class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name..'}))
    last_name  = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name..'}))
    email      = forms.EmailField(label='',help_text='Note: your Email will be hidden', widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    password1 = forms.CharField(label='',max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password..'}))
    password2 = forms.CharField(label='',max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password..'}))

    class Meta:
        model  = UserModel
        fields = ['first_name','last_name','email','password1','password2']
        
        
