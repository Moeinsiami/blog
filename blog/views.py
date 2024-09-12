from django.shortcuts import render
from blog.models import Post
from django.http import Http404


def index(request):
    pass


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    render(request, '', context)


def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except:
        raise Http404('Post does not exist')
    context = {
        'post': post,
    }
    render(request, '', context)