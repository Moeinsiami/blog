from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from blog.models import *
from blog.forms import *


def index(request):
    pass


# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 1)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context = {
#         'posts': posts,
#     }
#     return render(request, 'blog/list.html', context)

class PostListView(ListView):
    queryset = Post.published.all
    paginate_by = 2
    template_name = 'blog/list.html'
    context_object_name = 'posts'


# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
#     context = {
#         'post': post,
#     }
#     return render(request, 'blog/detail.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'


def ticket(request):
    ticket_obj = Ticket.objects.create()
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            redirect('blog:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html',{'form':form})
