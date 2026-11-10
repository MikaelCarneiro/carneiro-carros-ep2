from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("selecao/", views.PostListView.as_view(template_name="blog/selection.html"), name="selection"),
    path("sobre/", views.PostListView.as_view(template_name="blog/about.html"), name="about"),
    path("posts/novo/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/excluir/", views.PostDeleteView.as_view(), name="post_delete"),
    path("posts/<int:pk>/comentar/", views.CommentCreateView.as_view(), name="comment_create"),
    path("categorias/", views.CategoryListView.as_view(), name="category_list"),
    path("categorias/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
