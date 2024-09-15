from django.shortcuts import render, get_object_or_404
from blog.models import Post


def index(request):
    pass


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
