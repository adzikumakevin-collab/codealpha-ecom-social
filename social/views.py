from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from social.models import Post, Comment, Like

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
