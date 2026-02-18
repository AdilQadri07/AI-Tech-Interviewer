from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register_view(request):
    if request.method=='POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request,'accounts/register.html')

def login_view(request):
    if request.method=='POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request,user)
            return redirect('home') 
    return render(request,'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
