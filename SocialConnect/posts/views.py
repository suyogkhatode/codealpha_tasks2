from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import PostForm
from .models import Post, Like
from .models import Post, Like, Comment

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('home')

    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
@login_required

def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    return redirect('home')

@login_required
def add_comment(request, post_id):

    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        text = request.POST.get("comment")

        if text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )

    return redirect("home")
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, "post_detail.html", {"post": post})