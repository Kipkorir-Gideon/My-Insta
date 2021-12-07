from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm 
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required(login_url='/accounts/login/')
def homepage(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=request.user)
        comment_form = CommentForm(request.POST, instance=request.user)
        if post_form.is_valid():
            post_form.save()
            messages.success(request,('Your post has been added successfully.'))
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request,('Comment added successfully.'))
        post_id = request.POST.get('post_id')
        post = Image.objects.get(id=post_id)
        request.user.profile.posts.add(post)
        messages.success(request,(f'{post} added to your posts.'))
        return redirect('homePage')
    posts = Image.objects.all()
    post_form = PostForm(instance=request.user)
    comment_form = CommentForm(instance=request.user)
    return render(request, 'home.html', {'posts': posts, 'post_form': post_form, 'comment_form': comment_form})


@login_required
def posting(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
    return redirect('homePage')


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



@login_required
def commenting(request, image_id):
    comment_form = CommentForm()
    image = Image.objects.filter(pk=image_id).first()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.image = image 
            comment.save()
    return redirect("homePage")  


@login_required
def all_comments(request, image_id):
    image = Image.objects.filter(pk=image_id).first()
    return render(request,'comments.html',{'image':image})



@login_required
def likes(request,image_id):
    if request.method == 'GET':
        image = Image.objects.get(pk=image_id)
        user = request.user
        check_user = Likes.objects.filter(user=user,image=image).first()
        if check_user == None:
            image = Image.objects.get(pk=image_id)
            like = Likes(like=True,image=image,user=user)
            like.save()
            return JsonResponse({'success': True,'image':image_id,'status':True})
        else:
            check_user.delete()
            return JsonResponse({'success':True,'image':image_id,'status':False})



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
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request,('Your wishlist was successfully updated!'))
        else:
            messages.error(request,('Unable to complete request'))
        return redirect ("userpage")
    user = request.user
    posts = Image.objects.filter(user_id=user.id).all()
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_page.html', {'user':request.user, 'posts': posts, 'user_form':user_form, 'profile_form':profile_form})


@login_required
def search(request):
  if 'search_user' in request.GET and request.GET["search_user"]:
    name = request.GET.get('search_user')
    the_users = Profile.search_profiles(name)
    images = Image.search_images(name)
    print(the_users)
    return render(request, 'search.html', {"users": the_users, "images": images})
  else:
    return render(request, 'search.html')