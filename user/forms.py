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
        
        
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#a-full-example
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
    