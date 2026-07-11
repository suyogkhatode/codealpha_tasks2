from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Profile, Follow
from posts.models import Post


# ---------------- HOME ----------------

@login_required
def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"posts": posts})


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.get_or_create(user=user)

        login(request, user)

        return redirect("home")

    return render(request, "register.html")


# ---------------- LOGIN ----------------

def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "login.html")


# ---------------- LOGOUT ----------------

def logout_user(request):
    logout(request)
    return redirect("login")


# ---------------- PROFILE ----------------

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        profile.bio = request.POST.get("bio")
        profile.location = request.POST.get("location")

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        return redirect("profile")

    followers = Follow.objects.filter(following=request.user).count()
    following = Follow.objects.filter(follower=request.user).count()

    return render(request, "profile.html", {
        "profile": profile,
        "followers": followers,
        "following": following,
    })


# ---------------- USER PROFILE ----------------

@login_required
def user_profile(request, username):

    profile_user = get_object_or_404(User, username=username)

    profile = Profile.objects.get(user=profile_user)

    posts = Post.objects.filter(user=profile_user).order_by("-created_at")

    followers = Follow.objects.filter(following=profile_user).count()
    following = Follow.objects.filter(follower=profile_user).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(request, "user_profile.html", {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "followers": followers,
        "following": following,
        "is_following": is_following,
    })


# ---------------- FOLLOW / UNFOLLOW ----------------

@login_required
def follow_user(request, username):

    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:

        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        )

        if follow.exists():
            follow.delete()
        else:
            Follow.objects.create(
                follower=request.user,
                following=user_to_follow
            )

    return redirect("user_profile", username=username)