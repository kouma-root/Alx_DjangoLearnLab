from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

#Extend usercreationform with email

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
#Register view

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else :
        form = CustomUserCreationForm()
        return render(request, 'blog/register.html', {'form': form})
    
    

#Profil view
@login_required
def profile(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.save()
        return redirect('profile')
    return render(request, 'blog/profile.html')


