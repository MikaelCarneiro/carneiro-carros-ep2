import os
from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from blog.models import Category, Comment, Post, PostPhoto


AUTHORS = ("ana_leitora", "bruno_leitor")
EP1 = "https://gitlab.uspdigital.usp.br/14599342/carneiro-carros/-/"
EP1_REVISION = "2167179d144e1ab7a8544dcfa91bed35703765e4"
ARTICLES = (
    (
        6,
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
        {
            "url": f"{EP1}raw/{EP1_REVISION}/static/images/civic-br-frente.jpg",
            "credit": "Emerson Santos / Go Garage",
            "source_url": f"{EP1}blob/{EP1_REVISION}/content/carros/civic.md",
        },
    ),
    (
        7,
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
        {
            "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d7/Brazilian_Fiat_Uno_-_1999_model-year_-_side_and_front.jpg/960px-Brazilian_Fiat_Uno_-_1999_model-year_-_side_and_front.jpg",
            "credit": "Cauã Bassin / Wikimedia Commons",
            "source_url": "https://commons.wikimedia.org/wiki/File:Brazilian_Fiat_Uno_-_1999_model-year_-_side_and_front.jpg",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
        },
    ),
    (
        8,
        "Volkswagen Gol G3: um compacto brasileiro",
        "<p>O Gol G3 faz parte da memória de quem cresceu vendo compactos nacionais nas ruas. "
        "É também um bom exemplo de como uma mesma família reúne versões para usos diferentes.</p>"
        "<p>Na pesquisa de um exemplar, a identificação da versão vem antes da comparação de preço e equipamentos.</p>",
        ("Compactos",),
        (),
        {
            "url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/83/Volkswagen_Gol_1.0_Sport_2000_%2812940044984%29.jpg/960px-Volkswagen_Gol_1.0_Sport_2000_%2812940044984%29.jpg",
            "credit": "order_242 / Wikimedia Commons",
            "source_url": "https://commons.wikimedia.org/wiki/File:Volkswagen_Gol_1.0_Sport_2000_(12940044984).jpg",
            "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
        },
    ),
    (
        9,
        "Toyota Corolla XEi 2005",
        "<p>O Corolla é o sedã de proposta familiar da seleção original. Nesta ficha, o XEi "
        "combina motor 1.8 de 136 cv e câmbio manual.</p>"
        "<p>Vale observar o espaço interno e o conforto, além da diferença de potência e de "
        "transmissão em relação ao Civic LX automático da mesma seleção.</p>",
        ("Sedãs",),
        (
            ("ana_leitora", "Gostei da comparação entre os dois sedãs."),
            ("bruno_leitor", "A indicação do câmbio ajuda a identificar a versão da ficha."),
        ),
        {
            "url": f"{EP1}raw/{EP1_REVISION}/static/images/corolla-br-frente.jpg",
            "credit": "Carro Repasse",
            "source_url": f"{EP1}blob/{EP1_REVISION}/content/carros/corolla.md",
        },
    ),
    (
        9,
        "Volkswagen Golf 1.6 2005",
        "<p>O Golf é o hatch da seleção original. O exemplar de referência usa motor 1.6 "
        "de 101 cv e câmbio manual.</p>"
        "<p>As dimensões mais compactas oferecem um contraponto aos dois sedãs da seleção. "
        "O Golf e o Gol G3 têm fichas separadas por serem modelos distintos.</p>",
        ("Compactos",),
        (
            ("bruno_leitor", "A ficha ajuda a distinguir o Golf do Gol da outra publicação."),
            ("ana_leitora", "É interessante comparar o hatch com os dois sedãs de 2005."),
        ),
        {
            "url": f"{EP1}raw/{EP1_REVISION}/static/images/golf-br-frente.jpg",
            "credit": "Sul MF Multimarcas / Kleber Carros",
            "source_url": f"{EP1}blob/{EP1_REVISION}/content/carros/golf.md",
        },
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
        for day, title, content, labels, comments, photo in ARTICLES:
            post, created = Post.objects.get_or_create(title=title, defaults={"content": content})
            PostPhoto.objects.get_or_create(post=post, defaults=photo)
            if not created:
                continue
            Post.objects.filter(pk=post.pk).update(
                published_at=datetime(2026, 11, day, 16, tzinfo=zone)
            )
            post.categories.set([categories[label] for label in labels])
            for minute, (author, message) in enumerate(comments, start=1):
                comment = Comment.objects.create(post=post, author=users[author], text=message)
                Comment.objects.filter(pk=comment.pk).update(
                    published_at=datetime(2026, 11, day, 17, minute, tzinfo=zone)
                )

        if password := os.getenv("DJANGO_SUPERUSER_PASSWORD"):
            username = os.getenv("DJANGO_SUPERUSER_USERNAME", "administrador")
            if not User.objects.filter(username=username).exists():
                candidate = User(username=username)
                validate_password(password, candidate)
                User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS("Dados de demonstração disponíveis."))
