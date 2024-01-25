from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    sender_name     = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Name..'}))
    sender_email    = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    sender_message  = forms.CharField(label='', widget = forms.Textarea(attrs={'rows': 5,
                                                                              'class':'form-control',
                                                                              'placeholder': 'Your Message .. '}))
                                                                                                                                                                                                    
    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'sender_email', 'sender_message']
    
    
    
    
   
    