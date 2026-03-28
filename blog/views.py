
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, Story
from .forms import PostForm, CommentForm, StoryForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Post, Story, Profile

# Homepage (optional)
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'stories': stories})


#  ALL POSTS PAGE

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts})


#  STORIES PAGE

def all_stories(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'stories.html', {'stories': stories})


#  PROFILE PAGE (UPLOAD IMAGE)
@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        image = request.FILES.get('image')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        dob = request.POST.get('dob')

        # update image
        if image:
            profile.image = image

        profile.bio = bio
        profile.location = location

        # only save DOB if provided
        if dob:
            profile.dob = dob

        # validation message
        if image and (not location or not dob):
            messages.warning(request, "You must also set Location and Date of Birth.")
        else:
            messages.success(request, "Profile updated successfully.")

        profile.save()

    return render(request, 'profile.html', {'profile': profile})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('home')
    return render(request, 'create_post.html', {'form': form})

@login_required
def create_story(request):
    form = StoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        story = form.save(commit=False)
        story.user = request.user
        story.save()
        return redirect('home')
    return render(request, 'create_story.html', {'form': form})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()

    likes = Like.objects.filter(post=post).count()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'likes': likes
    })

@login_required
def like_post(request, id):
    post = Post.objects.get(id=id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('post_detail', id=id)


@login_required
def react_post(request, id):

    post = Post.objects.get(id=id)
    emoji = request.POST.get('emoji')

    Like.objects.update_or_create(
        user=request.user,
        post=post,
        defaults={'emoji': emoji}
    )

    return redirect('post_detail', id=id)

@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'my_posts.html', {'posts': posts})

@login_required
def delete_post(request, id):
    post = Post.objects.get(id=id, user=request.user)
    post.delete()
    return redirect('my_posts')

@login_required
def edit_post(request, id):
    post = Post.objects.get(id=id, user=request.user)

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        return redirect('my_posts')

    return render(request, 'edit_post.html', {'post': post})

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_comment(request, id):
    post = Post.objects.get(id=id)

    if request.method == "POST":
        text = request.POST.get('text')
        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

    return redirect('post_detail', id=id)