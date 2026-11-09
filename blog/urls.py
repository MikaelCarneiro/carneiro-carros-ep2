from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("posts/novo/", views.post_create, name="post_create"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/editar/", views.post_update, name="post_update"),
    path("posts/<int:pk>/excluir/", views.post_delete, name="post_delete"),
]
