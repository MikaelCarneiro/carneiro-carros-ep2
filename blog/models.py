from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField("título", max_length=180)
    content = models.TextField("conteúdo HTML")
    published_at = models.DateTimeField("data de postagem", auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-pk"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("comentário", max_length=1500)
    published_at = models.DateTimeField("data de postagem", auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-pk"]
        verbose_name = "comentário"
        verbose_name_plural = "comentários"

    def __str__(self):
        return f"{self.author} em {self.post}"
