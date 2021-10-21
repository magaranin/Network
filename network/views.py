from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm

from .models import User, Post
from django.contrib.auth.decorators import login_required
from .forms import CreateNewPostForm

def index(request):
    # Authenticated users view the posts
    if request.user.is_authenticated:
        posts = Post.objects.order_by("-created_date").all()
        return render(request, "network/index.html", {
            "posts": posts
        })

    # Everyone else is promped to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        #first_name = request.POST["first_name"]
        #last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def create_new_post(request):
    if request.method == "POST":
        form = CreateNewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/create_new_post.html", {
            "form": CreateNewPostForm()
        })

@login_required
def profile_page(request, profile_owner_id):
    profile_owner = User.objects.get(pk=profile_owner_id)
    is_followed = request.user.followed_users.filter(pk=profile_owner_id).exists()
    posts = Post.objects.filter(
            owner = profile_owner
        )
    posts = posts.order_by("-created_date").all()
    return render(request, "network/profile_page.html" ,{
        "is_followed": is_followed,
        "profile_owner": profile_owner,        
        "posts": posts
    })


@login_required
def update_follows(request, profile_owner_id):
    if request.method == "POST":
        user = request.user # follow -unfollow profile_owner
        is_followed = user.followed_users.filter(pk=profile_owner_id).exists()
        profile_owner = User.objects.get(pk=profile_owner_id)
        if is_followed:
            user.followed_users.remove(profile_owner) 
            profile_owner.followers.remove(user)
        else:
            user.followed_users.add(profile_owner) 
            profile_owner.followers.add(user)
    return HttpResponseRedirect(reverse("profile_page", args=(profile_owner_id,)))


@login_required
def following(request):
    #user = request.user # account logged in
    followed_users = request.user.followed_users.all()
    posts = Post.objects.filter(
            owner__in = followed_users
        )
    return render(request, "network/following.html", {    
        "posts": posts
    })