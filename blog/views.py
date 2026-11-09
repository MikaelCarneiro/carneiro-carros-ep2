from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_safe, require_http_methods

from .models import Post


@require_safe
def post_list(request):
    return render(request, "blog/post_list.html", {"posts": Post.objects.all()})


@require_safe
def post_detail(request, pk):
    return render(request, "blog/post_detail.html", {"post": get_object_or_404(Post, pk=pk)})


@permission_required("blog.add_post", raise_exception=True)
@require_http_methods(["GET", "HEAD", "POST"])
def post_create(request):
    if request.method == "POST":
        post = Post.objects.create(
            title=request.POST["title"], content=request.POST["content"]
        )
        return redirect("blog:post_detail", pk=post.pk)
    return render(request, "blog/post_form.html")


@permission_required("blog.change_post", raise_exception=True)
@require_http_methods(["GET", "HEAD", "POST"])
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()
        return redirect("blog:post_detail", pk=pk)
    return render(request, "blog/post_form.html", {"post": post})


@permission_required("blog.delete_post", raise_exception=True)
@require_http_methods(["GET", "HEAD", "POST"])
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
