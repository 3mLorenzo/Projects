from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, Like


def index(request):
    all_posts = Post.objects.all().order_by('id').reverse()

    p = Paginator(all_posts, 10)
    page = request.GET.get('page')
    page_posts = p.get_page(page)

    likes = Like.objects.all()
    liked = []

    try: 
        for a in likes:
            if a.user.id == request.user.id:
                liked.append(a.post.id)
    except:
        liked = []

    return render(request, "network/index.html", {
        "all_posts":all_posts,
        "page_posts":page_posts,
        "liked":liked,
        "likes":likes
    })

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit = Post.objects.get(pk=post_id)
        edit.content = data["content"]
        edit.save()
        return JsonResponse({"message": "Post edited!", "data": data["content"]})

def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        k = Post(content=content, owner=user)
        k.save()
        return HttpResponseRedirect(reverse(index))

def following(request):
    user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(user1=user)
    posts = Post.objects.all().order_by("id").reverse()

    related_posts = []

    likes = Like.objects.all()
    liked = []

    try: 
        for a in likes:
            if a.user.id == request.user.id:
                liked.append(a.post.id)
    except:
        liked = []

    for post in posts:
        for follow in following:
            if follow.user2 == post.owner:
                related_posts.append(post)
    
    p = Paginator(related_posts, 10)
    page = request.GET.get('page')
    page_posts = p.get_page(page)

    return render(request, "network/following.html", {
        "page_posts":page_posts,
        "liked":liked,
        "likes":likes
    })

def r_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    f = Like.objects.filter(user=user, post=post)
    f.delete()

    return JsonResponse({"message": "Disliked!"})

def a_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    f = Like(user=user, post=post)
    f.save()

    return JsonResponse({"message": "Liked!"})

def profile_page(request, user_id):

    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(owner=user).order_by('id').reverse()

    following = Follow.objects.filter(user1=user)
    followed = Follow.objects.filter(user2=user)

    likes = Like.objects.all()
    liked = []

    try: 
        for a in likes:
            if a.user.id == request.user.id:
                liked.append(a.post.id)
    except:
        liked = []

    try:
        follow = followed.filter(user1=User.objects.get(pk=request.user.id))
        if len(follow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    p = Paginator(all_posts, 10)
    page = request.GET.get('page')
    page_posts = p.get_page(page)


    return render(request, "network/profile_page.html", {
        "all_posts":all_posts,
        "page_posts":page_posts,
        "username":user.username,
        "following":following,
        "followed":followed,
        "is_following":is_following,
        "profile":user,
        "likes":likes,
        "liked":liked
    })

def follow(request):
    user_follow = request.POST['user_follow']
    user = User.objects.get(pk=request.user.id)
    user_data = User.objects.get(username=user_follow)

    f = Follow(user1=user, user2=user_data)
    f.save()

    id = user_data.id

    return HttpResponseRedirect(reverse(profile_page, kwargs={ "user_id":id }))

def unfollow(request):
    user_follow = request.POST['user_follow']
    user = User.objects.get(pk=request.user.id)
    user_follower = User.objects.get(username=user_follow)

    f = Follow.objects.get(user1=user, user2=user_follower)
    f.delete()

    id = user_follower.id

    return HttpResponseRedirect(reverse(profile_page, kwargs={ "user_id":id}))


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
