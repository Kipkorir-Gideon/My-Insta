from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='/accounts/login/')
def homepage(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=request.user)
        comment_form = CommentForm(request.POST, instance=request.user)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, ('Your post has been added successfully.'))
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, ('Comment added successfully.'))
        return redirect('homePage')
    posts = Image.objects.all()
    post_form = PostForm(instance=request.user)
    comment_form = CommentForm(instance=request.user)
    return render(request, 'home.html', {'posts': posts, 'post_form': post_form, 'comment_form': comment_form})


@login_required
def posting(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('homePage')
    else:
        post_form = PostForm()
    return render(request, 'post.html', {"post_form": post_form})


@login_required
def commenting(request, image_id):
    comment_form = CommentForm()
    image = Image.objects.filter(pk=image_id).first()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.photo = image
            comment.save()
    return redirect("homePage")


@login_required
def all_comments(request, image_id):
    image = Image.objects.filter(pk=image_id).first()
    return render(request, 'comments.html', {'image': image})


@login_required
def likes(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    like = Likes.objects.filter(image=image, liker=request.user).first()
    if like is None:
        like = Likes()
        like.image = image
        like.liker = request.user
        like.save()
    else:
        like.delete()
    return redirect('homePage')


def user_page(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(
                request, ('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(
                request, ('Your wishlist was successfully updated!'))
        else:
            messages.error(request, ('Unable to complete request'))
        return redirect("userpage")
    user = request.user
    comment_form = CommentForm()
    posts = Image.objects.filter(user_id=user.id).all()
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_page.html', {'user': request.user, 'posts': posts, 'user_form': user_form, 'profile_form': profile_form, 'comment_form': comment_form})


@login_required
def users_profile(request, pk):
    comment_form = CommentForm()
    user = User.objects.get(pk=pk)
    images = Image.objects.filter(user=user)
    c_user = request.user

    return render(request, 'users_profile.html', {"user": user, "images": images, "c_user": c_user, 'comment_form': comment_form})


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
