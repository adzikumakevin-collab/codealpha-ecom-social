from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .models import Post, Comment, Follow   

def home_feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'social/feed.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content:
            Post.objects.create(author=request.user, content=content, image=image)
            return redirect('home_feed')
    return render(request, 'social/create_post.html')

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('home_feed')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('home_feed')
from .models import Follow # Assure-toi de rajouter Follow dans tes imports en haut

@login_required
def user_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user_profile).order_by('-created_at')
    
    # Vérifier si l'utilisateur connecté suit déjà ce profil
    is_following = Follow.objects.filter(follower=request.user, user=user_profile).exists()
    
    context = {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'is_following': is_following,
        'followers_count': user_profile.followers.count(),
        'following_count': user_profile.following.count(),
    }
    return render(request, 'social/profile.html', context)

@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        follow_record = Follow.objects.filter(follower=request.user, user=user_to_follow)
        if follow_record.exists():
            follow_record.delete()  # Se désabonner
        else:
            Follow.objects.create(follower=request.user, user=user_to_follow)  # S'abonner
    return redirect('user_profile', username=username)