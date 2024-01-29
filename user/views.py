from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from blogger.settings import DEFAULT_FROM_EMAIL
from django.utils.encoding import smart_bytes
from .forms import UserModelForm, UserLoginForm, EmailForm, ProfileUpdateForm, UserModelUpdateForm
from django.utils.encoding import smart_str
from .models import UserModel,Profile 


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
           last_name  = form.cleaned_data['last_name']
           email      = form.cleaned_data['email']
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
def send_confirm_email_link_manuall(request):
    
        if request.method == 'POST' :
            form = EmailForm(request.POST)
            if form.is_valid():
                email    = request.POST.get('email')      
                user = UserModel.objects.get(email=email) 
                if user is not None and user.is_confirmEmail == False :
                    
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
                    messages.success(request,f'( {user.first_name} ), please go to your email {user.email} to comlete the registeration')  
                    return redirect('user:user-login')

                
                if user is not None and user.is_confirmEmail == True :
                    return redirect('user:user-login')
        
        else:
            form = EmailForm()   
        
        context = {
            'form' : form,
        }
        return render(request,'user/send_confirm_email_link_button.html', context=context)




# this function is work after the user open his email and click on link inside 
# check before login - work after the email reach to user and he clik the link inside it 
###################### EmailConfirmAPIView #################
def confirmEmail_and_activateUser(request,uidb64,token):
    print('uidb64='+uidb64)
    print('token='+token) 
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        print(uid)
        #user = get_user_model().objects.get(pk=uid)
        user = UserModel.objects.get(id=uid)
        print(user)
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
        return redirect('user:send-confirm-email-link-manuall')





def user_login(request):
    if request.method == 'POST':
        form     = UserLoginForm(request.POST)
        email    = request.POST.get('email')     # must be confirm email to can login
        password = request.POST.get('password')
        
        user = authenticate(request,username=email,password=password)
        #print(user)
        #user = UserModel.objects.get(email=email)
        print(user)
        if user is not None and user.is_confirmEmail == True :
            print('user='+ str(user))
            login(request,user)
            form = UserLoginForm()
            messages.success(request,f'welcome back {user.get_user_fullname} you do login successfully.')
            return redirect('blog:home')
           
        
        if user is not None and user.is_confirmEmail == False:
            messages.error(request,f'email or password not correct, or your email not confirm')
            return redirect('user:send-confirm-email-link-manuall')
        
        else:
            messages.error(request,f'Error in email or password!')
            return redirect('user:user-login')
            
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


def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile' : profile,
    }
    return render(request,'user/profile.html',context)



def my_profile_usermodel_update(request):
    instance_user    = request.user
    instance_profile = get_object_or_404(Profile, user=instance_user)
    
    userform    = UserModelUpdateForm(instance=instance_user)
    profileform = ProfileUpdateForm(instance=instance_profile)
    
    if request.method == 'POST' :
        userform    = UserModelUpdateForm(request.POST, instance=instance_user)
        profileform = ProfileUpdateForm(request.POST, instance=instance_profile)
        if userform.is_valid() and  profileform.is_valid():
           updated_user = userform.save()
           update_profile = profileform.save()
           messages.success(request,f'you update your profile and user successfully')
           form = UserModelForm()
           return redirect('user:my-profile')
     
    context = {
        'userform'   : userform,
        'profileform': profileform,
    }
    return render(request,'user/profile_usermodel_update.html',context)