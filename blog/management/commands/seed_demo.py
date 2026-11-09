import os
from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from blog.models import Category, Comment, Post


AUTHORS = ("ana_leitora", "bruno_leitor")
ARTICLES = (
    (
        "Honda Civic LX 2005",
        "<p>O Civic começou a ser produzido no Brasil em Sumaré, em 1997. "
        "Esta publicação destaca o LX automático do ano modelo 2005.</p>"
        "<p>Com motor 1.7 de 115 cv e câmbio automático de quatro marchas, "
        "o LX ocupava a entrada da linha. As versões LXL e EX usavam "
        "o motor VTEC de 130 cv.</p>"
        "<p><strong>Ficha do LX:</strong> 15,2 kgfm de torque, "
        "1.165 kg e tração dianteira. A ficha da primeira entrega "
        "registra a FIPE de R$ 26.835,00 em agosto de 2026.</p>",
        ("Anos 2000", "Sedãs"),
        (
            ("ana_leitora", "A comparação com a versão EX ajuda a entender a linha."),
            ("bruno_leitor", "Gostei de ver qual versão serve de referência para a ficha."),
            ("ana_leitora", "O câmbio de quatro marchas é um detalhe interessante dessa geração."),
        ),
    ),
    (
        "Fiat Uno: simplicidade no dia a dia",
        "<p>O Uno é um bom ponto de partida para conversar sobre os compactos. "
        "A proposta valoriza espaço útil e facilidade para circular na cidade.</p>"
        "<p>Na hora de comparar exemplares usados, vale separar a versão, "
        "o ano e o histórico de manutenção.</p>",
        ("Anos 2000", "Compactos"),
        (
            ("bruno_leitor", "O tamanho compacto é uma vantagem para estacionar."),
            ("ana_leitora", "Separar as versões evita comparar carros diferentes."),
        ),
    ),
    (
        "Volkswagen Gol G3: um compacto brasileiro",
        "<p>O Gol G3 faz parte da memória de quem cresceu vendo compactos nacionais nas ruas. "
        "É também um bom exemplo de como uma mesma família reúne versões para usos diferentes.</p>"
        "<p>Na pesquisa de um exemplar, a identificação da versão vem antes da comparação de preço e equipamentos.</p>",
        ("Compactos",),
        (),
    ),
)


class Command(BaseCommand):
    help = "Preenche o blog de demonstração sem substituir registros existentes."

    def add_arguments(self, parser):
        parser.add_argument("--require-existing-users", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        users = {}
        for username in AUTHORS:
            if options["require_existing_users"]:
                try:
                    users[username] = User.objects.get(username=username)
                except User.DoesNotExist as error:
                    raise CommandError(f"Crie {username} no administrador primeiro.") from error
            else:
                user, created = User.objects.get_or_create(username=username)
                if created:
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
                users[username] = user

        categories = {}
        for name, description in (
            ("Anos 2000", "Publicações sobre carros presentes no Brasil na década de 2000."),
            ("Compactos", "Carros compactos e suas propostas para o dia a dia."),
            ("Sedãs", "Publicações sobre sedãs e suas versões."),
        ):
            categories[name], _ = Category.objects.get_or_create(
                name=name, defaults={"description": description}
            )

        zone = ZoneInfo("America/Sao_Paulo")
        for index, (title, content, labels, comments) in enumerate(ARTICLES):
            post, created = Post.objects.get_or_create(title=title, defaults={"content": content})
            if not created:
                continue
            Post.objects.filter(pk=post.pk).update(
                published_at=datetime(2026, 11, 6 + index, 16, tzinfo=zone)
            )
            post.categories.set([categories[label] for label in labels])
            for minute, (author, message) in enumerate(comments, start=1):
                comment = Comment.objects.create(post=post, author=users[author], text=message)
                Comment.objects.filter(pk=comment.pk).update(
                    published_at=datetime(2026, 11, 6 + index, 17, minute, tzinfo=zone)
                )

        if password := os.getenv("DJANGO_SUPERUSER_PASSWORD"):
            username = os.getenv("DJANGO_SUPERUSER_USERNAME", "administrador")
            if not User.objects.filter(username=username).exists():
                candidate = User(username=username)
                validate_password(password, candidate)
                User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS("Dados de demonstração disponíveis."))
