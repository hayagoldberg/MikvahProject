from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from .forms import SignupForm
from django.urls import reverse


# Create your views here.

def signup_view(request):
    # Signup view to register new users and sort them on 2 groups: client and professional
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            group_professional = Group.objects.get(name='Professional')
            group_client = Group.objects.get(name='Client')
            if group_professional in user.groups.all(): # if the user choose a pro account
                login(request, user)
                return redirect('website:pro_page') # redirect to the pro page
            elif group_client in user.groups.all(): # if the uer choose a client account
                login(request, user)
                return redirect('website:client_page') # redirect to the client page
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {"form": form})


def login_view(request):
    # login the user and redirect him to the right page (client or pro)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # log the user in and redirect
            if user.groups.filter(name='Professional').exists():
                return redirect('website:pro_page')
            elif user.groups.filter(name='Client').exists():
                return redirect('website:client_page')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {"form": form})


def logout_view(request):
    # logout the user and redirect to the homepage
    if request.method == "POST":
        logout(request)
        return render(request, 'website/index.html')