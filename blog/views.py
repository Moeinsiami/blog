from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth import authenticate, login
from blog.models import *
from blog.forms import *


def index(request):
    return render(request, 'blog/index.html')


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    print(posts, type(posts))
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, "blog/list.html", context)

# class PostListView(ListView):
#     queryset = Post.published.all
#     # paginate_by = 2
#     template_name = 'blog/list.html'
#     context_object_name = 'posts'


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'


def ticket(request):
    if request.method == "POST":

        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'], phone=cd['phone'],
                                  subject=cd['subject'])
            # ticket_obj.message = cd['message']
            # ticket_obj.name = cd['name']
            # ticket_obj.email = cd['email']
            # ticket_obj.phone = cd['phone']
            # ticket_obj.subject = cd['subject']
            # ticket_obj.save()
            return redirect('blog:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment.html', context)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query)).filter(
                similarity__gte=0.1).order_by('-similarity')
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)

    return render(request, 'blog/profile.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            post.save()
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')
    return render(request, 'forms/delete-post.html', {'post': post})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':

        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            post.save()
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create_post.html', {'form': form, 'post': post})


# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse('Your account is disabled')
#             else:
#                 return HttpResponse('You are not logged in')
#
#     else:
#         form = LoginForm()
#     return render(request, 'forms/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {
        'account_form': account_form,
        'user_form': user_form
    }
    return render(request, 'registration/edit_account.html', context)
