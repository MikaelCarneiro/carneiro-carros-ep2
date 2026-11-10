from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Comment, Post, PostPhoto


def url(name, pk=None):
    return reverse(f"blog:{name}", args=[] if pk is None else [pk])


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.editor = User.objects.create_superuser("editor")
        cls.reader = User.objects.create_user("leitora")
        cls.post = Post.objects.create(title="Civic", content="<p>Ficha <strong>HTML</strong></p>")
        cls.category = Category.objects.create(name="Sedãs", description="Carros sedã")
        cls.post.categories.add(cls.category)
        cls.other = Post.objects.create(title="Outro post", content="<p>Outro conteúdo</p>")

    def test_public_list_detail_and_missing_urls(self):
        self.assertContains(self.client.get(url("post_list")), self.post.title)
        self.assertContains(self.client.get(self.post.get_absolute_url()), "<strong>HTML</strong>")
        for name in ("post_detail", "category_detail", "comment_create"):
            self.assertEqual(self.client.get(url(name, 999999)).status_code, 404)

    def test_crud_requires_permissions(self):
        for name, pk in (("post_create", None), ("post_update", self.post.pk), ("post_delete", self.post.pk)):
            self.assertEqual(self.client.get(url(name, pk)).status_code, 302)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post(url("post_create"), {"title": "Intruso"}).status_code, 403)
        self.assertEqual(self.client.post(url("post_delete", self.post.pk)).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_create_validate_edit_confirm_and_delete(self):
        self.client.force_login(self.editor)
        self.assertEqual(self.client.post(url("post_create"), {"title": "", "content": ""}).status_code, 200)
        self.assertEqual(Post.objects.count(), 2)
        created = self.client.post(url("post_create"), {
            "title": "Novo", "content": "<p>Original</p>", "categories": [self.category.pk],
        })
        post = Post.objects.get(title="Novo")
        self.assertRedirects(created, post.get_absolute_url())
        self.assertEqual(list(post.categories.all()), [self.category])
        self.assertRedirects(self.client.post(url("post_update", post.pk), {
            "title": "Editado", "content": "<p>Alterado</p>", "categories": [self.category.pk],
        }), post.get_absolute_url())
        post.refresh_from_db()
        self.assertEqual(post.title, "Editado")
        confirmation = self.client.get(url("post_delete", post.pk))
        self.assertContains(confirmation, "Confirmar exclusão")
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertRedirects(self.client.post(url("post_delete", post.pk)), url("post_list"))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_authenticated_comment_preserves_author_and_order_and_escapes_html(self):
        Comment.objects.create(post=self.post, author=self.editor, text="Mensagem anterior")
        target = url("comment_create", self.post.pk)
        self.assertEqual(self.client.post(target, {"text": "Anônimo"}).status_code, 302)
        self.client.force_login(self.reader)
        self.assertContains(self.client.get(target), "Novo comentário")
        response = self.client.post(target, {"text": "<script>alert(1)</script>", "author": self.editor.pk})
        self.assertRedirects(response, self.post.get_absolute_url() + "#comentarios")
        self.assertEqual(self.post.comments.first().author, self.reader)
        rendered = self.client.get(self.post.get_absolute_url()).content.decode()
        self.assertNotIn("<script>alert(1)</script>", rendered)
        self.assertLess(rendered.index("&lt;script&gt;"), rendered.index("Mensagem anterior"))

    def test_category_reuses_list_and_filters_posts(self):
        categories = self.client.get(url("category_list"))
        self.assertContains(categories, url("category_detail", self.category.pk))
        self.assertNotContains(categories, self.post.get_absolute_url())
        self.assertNotContains(categories, "Todos os carros")
        response = self.client.get(url("category_detail", self.category.pk))
        self.assertTemplateUsed(response, "blog/post_list.html")
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, self.other.title)
        self.assertContains(self.client.get(self.post.get_absolute_url()), url("category_detail", self.category.pk))

    def test_navigation_uses_the_same_posts_and_photos(self):
        photo = PostPhoto.objects.create(post=self.post, url="https://example.com/civic.jpg", credit="Fotógrafo")

        self.assertRedirects(self.client.get(url("selection")), url("post_list"), status_code=301)
        for view_name in ("post_list", "about"):
            with self.subTest(view=view_name):
                response = self.client.get(url(view_name))
                self.assertContains(response, self.post.get_absolute_url())
                self.assertContains(response, self.other.get_absolute_url())
                self.assertContains(response, photo.url, count=1)
                self.assertNotContains(response, url("selection"))

        self.assertContains(self.client.get(self.post.get_absolute_url()), photo.url, count=1)
        category = self.client.get(url("category_detail", self.category.pk))
        self.assertContains(category, photo.url, count=1)
        self.assertNotContains(category, self.other.get_absolute_url())
