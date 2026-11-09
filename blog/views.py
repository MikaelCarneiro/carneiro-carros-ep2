from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "blog.add_post"
    model = Post
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "blog.change_post"
    model = Post
    form_class = PostForm


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "blog.delete_post"
    model = Post
    success_url = reverse_lazy("blog:post_list")
