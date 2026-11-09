from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("posts/novo/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/excluir/", views.PostDeleteView.as_view(), name="post_delete"),
]
