from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('user-register/', views.user_create, name='user-register'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('forget-password/', views.forget_password, name='forget-password'),
    
    # EmailConfirm
    path('confirm-email/<uidb64>/<str:token>/',views.confirmEmail_and_activateUser, name='confirmEmail_and_activateUser'),
    path('send_confirmation_email_manuall/<uidb64>/<str:token>/',views.send_confirmation_email_manuall, name='send-confirmation-email-manuall'),

]
