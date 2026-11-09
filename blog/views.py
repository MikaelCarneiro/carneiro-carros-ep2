from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


class PostListView(ListView):
    model = Post
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.select_related("author")
        context["comment_form"] = CommentForm()
        return context


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.target_post = get_object_or_404(Post, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(post=self.target_post, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.target_post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"{self.target_post.get_absolute_url()}#comentarios"


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"


class CategoryDetailView(PostListView):
    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.category.posts.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(category=self.category, **kwargs)
