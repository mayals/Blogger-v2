from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.decorators import login_required

from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from .forms import UserModelForm, UserLoginForm
from django.contrib.auth.tokens import default_token_generator

def user_create(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
           new_user = form.save(commit= False)
           password2 = form.cleaned_data['password2']
           new_user.set_password(password2)
           new_user.save()     # here new user is saved in database
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           email     = form.cleaned_data['email']
           messages.success(request,f'welcome( {first_name} {last_name} ), please go to your email {email} to comlete the registeration')
           form = UserModelForm()
           return redirect('blog:home')
       
        else:
            messages.error(request,f'user not created! please complete those fields below.!')
    
    context = {
            'form' : form ,
    }
    return render(request,'user/user_create.html',context = context)
    



# this function to send confim link to email of user manullay after user want of confirm his email
def send_confirmation_email_manuall(request):
    user = request.user   
    subject = 'Confirm Your Email Address'
    from_email = DEFAULT_FROM_EMAIL    # load_dotenv() - this work her to bring this variable value from file .env
    to_email = user.email
    message = render_to_string('user/email_confirmation.html', 
                                                            {
                                                            'user'  : user,
                                                            'domain': 'localhost:8000',
                                                            'uid'   : urlsafe_base64_encode(smart_bytes(user.pk)),
                                                            'token' : default_token_generator.make_token(user),
                                                            }
                                ) 
    send_mail(subject, message, from_email, [to_email], fail_silently=False)
        





# this function is work after the user open his email and click on link inside 
# check before login - work after the email reach to user and he clik the link inside it 
###################### EmailConfirmAPIView #################
def confirmEmail_and_activateUser(request,uidb64,token):
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request,f'User does not exist.!')
        return redirect('user:user-register')

    if default_token_generator.check_token(user,token):
        user.is_active = True
        user.is_confirmEmail = True
        user.save()
        messages.success(request,f'{user.get_user_fullname}! Thank you for your email confirmation. Now you are active user and can login your account.')
        return redirect('user:user-login')
          
    else:
        messages.error(request,f'Activation link is invalid.! please click on send button to send confirmation link to you email { user.email } to confirm Email ')
        
        return redirect('user:user-login')












def user_login(request):
    if request.method == 'POST':
        form     = UserLoginForm(request.POST)
        email    = request.POST.get('email')     # must be confirm email
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_confirmEmail and user.is_active == True :
            login(request,user)
            form = UserLoginForm()
            messages.success(request,f'welcome back {user.get_user_fullname} you do success login successfully.')
            return redirect('blog:home')
            #userprofile = get_object_or_404(UserProfile, user=user)
            #return redirect('users:edit-profile',prof_id=profile.id)
        
        else:
            messages.error(request,f'email or password not correct, or your email not confirm ')
    
    else:
        form = UserLoginForm()          
    
    context = {
            'form' : form,
    }
    return render(request,'user/user_login.html', context=context)



@login_required(login_url='user:user-login')
def user_logout(request):
    logout(request)
    return redirect('blog:home')



def forget_password(request):
    return render 