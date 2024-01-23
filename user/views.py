from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserModelForm


def user_create(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
           new_user = form.save(commit= False)
           password2 = form.cleaned_data['password2']
           new_user.set_password(password2)
           new_user.save()
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           messages.success(request,f'welcome( {first_name} {last_name} ), your user created successfully !')
           form = UserModelForm()
           return redirect('blog:home')
       
        else:
            messages.error(request,f'user not created! please complete those fields below.!')
    
    context = {
            'form' : form ,
    }
    return render(request,'user/user_create.html',context = context)
    #return redirect('user:user-register') # allso work after put arg ang kwarg



