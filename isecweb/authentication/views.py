from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return render(request, 'authentication/login.html')

def login_request(request):
    if request.user.is_authenticated:
        return redirect(reverse('home-page'))    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'login succeed :)')
                return redirect(reverse('home-page'))
    else:
        form = AuthenticationForm()
    form.fields['username'].widget.attrs = {'class':'form-control ', 'placeholder':'Enter username', 'required':'required', 'autofocus':'autofocus', 'id':'inputEmail'}
    form.fields['password'].widget.attrs = {'class':'form-control ', 'placeholder':'Enter Password', 'id':'inputPassword', 'required':'required'}
    context = {'form':form, 'auth':True}
    return render(request, 'authentication/login.html', context)

def signup_request(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, 'Registration Successful. Please Login In.')
            return redirect(reverse('auth-login'))
    else:
        form = CreateUserForm()
    form.fields['username'].widget.attrs = {'class':'form-control form-control-user', 'placeholder':'Enter username'}
    form.fields['email'].widget.attrs = {'class':'form-control form-control-user', 'placeholder':'Enter Email'}
    form.fields['password1'].widget.attrs = {'class':'form-control form-control-user', 'placeholder':'Enter password'}
    form.fields['password2'].widget.attrs = {'class':'form-control form-control-user', 'placeholder':'Confirm Password'}
    context = {'form':form, 'auth':True}
    return render(request, 'authentication/register.html', context)


def logout_request(request):
    logout(request)
    return redirect(reverse('auth-login'))

