from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("conta/", include("django.contrib.auth.urls")),
    path("", include("blog.urls")),
]

if settings.ON_RENDER:
    # Apenas os arquivos públicos coletados pelo Django, inclusive os do admin.
    urlpatterns += [
        path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
    ]
