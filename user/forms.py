from django import forms 
from .models import UserModel, Profile
from django.contrib.auth import get_user_model

## https: // pypi.org/project/django-bootstrap-datepicker-plus / 
## https: // monim67.github.io/django-bootstrap-datepicker-plus/configure / 
# from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput



class UserModelForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name..'}))
    last_name  = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name..'}))
    email      = forms.EmailField(label='',help_text='Note: your Email will be hidden', widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    password1  = forms.CharField(label='',max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password..'}))
    password  = forms.CharField(label='',max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password..'}))
    class Meta:
        model  = get_user_model()
        fields = ['first_name','last_name','email','password1','password']
        
        
    # https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#a-full-example
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password:
            raise forms.ValidationError("Your passwords do not match")
        return password
    
    
    
    
    
class UserLoginForm(forms.ModelForm):
    email    = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    password = forms.CharField(label='',max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password..'}))

    class Meta:
        model   = get_user_model()
        fields  = ("email", "password")
        
        
class EmailForm(forms.Form):
    email    = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email..'}))

    class Meta:
        fields  = ("email")
        
        




class UserModelUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name..'}))
    last_name  = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name..'}))
    class Meta:
        model  = get_user_model()
        fields = ['first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    bio  = forms.CharField(label='', widget = forms.Textarea(attrs={'rows': 5,
                                                                        'placeholder': 'Bio..'}))
    class Meta:
        model   = Profile
        fields  = ('bio', 'profile_pic', 'date_of_birth', 'gender', 'website', 'phone_number', 'country')
        widgets = {
            # specify date-frmat
            'date_of_birth': DatePickerInput(format='%Y-%m-%d'),
        }
