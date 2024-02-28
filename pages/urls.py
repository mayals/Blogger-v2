from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('contact_us/', views.contact_us, name='contact_us'),
    path('thank_you/', views.ThankTemplateView.as_view(), name='thank_you'),
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('privacy-police/', views.LicenceTemplateView.as_view(), name='licence'),


]