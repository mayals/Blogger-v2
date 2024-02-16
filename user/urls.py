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
    path('send-confirm-email-link-manuall/',views.send_confirm_email_link_manuall, name='send-confirm-email-link-manuall'),

    path('my-profile/',views.my_profile, name='my-profile'),
    path('my-profile-usermodel-update/',views.my_profile_usermodel_update, name='my-profile-usermodel-update'),

    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    
    
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]   
        
