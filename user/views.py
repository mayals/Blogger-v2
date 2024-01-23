from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserModelForm


def user_create(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
           new_user = form.save(commit= False)
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           new_user.set_password(password)
           new_user.save()
           messages.success(request,f'welcome( {username} ), your user created successfully !')
           return redirect('blog:home')
       
        else:
            messages.error(request,f'user not created! please complete those fields below.!')
    
    context = {
            'form' : form ,
    }
    return render(request,'user/user_create.html',context = context)
    #return redirect('user:user-register') # allso work after put arg ang kwarg



