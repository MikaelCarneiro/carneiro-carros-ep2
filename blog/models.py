from django.db import models


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
