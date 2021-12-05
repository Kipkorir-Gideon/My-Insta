from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm 
from .forms import NewUserForm, UserForm, ProfileForm

# Create your views here.
def homepage(request):
	return render(request=request, template_name='home.html')


def user_register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,'Registration successful.')
            return redirect("login")  
        messages.error(request,'Registration failed.')
    form = NewUserForm()
    return render(request, "registration/registration.html", {'register_form': form})


def user_login(request):
    if request.method == 'POST':
        form  = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect("homePage")
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request,'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, template_name='registration/login.html', context={'login_form':form})


def user_logout(request):
    logout(request)
    messages.info(request,'You have successfully logged out.')
    return redirect("login")


def user_page(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_page.html', {'user':request.user, 'user_form':user_form, 'profile_form':profile_form})