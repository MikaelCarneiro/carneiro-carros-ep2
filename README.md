# Carneiro Carros · EP2 de PMR3304

Blog em Django para a segunda entrega de laboratório. A página inicial, os posts e as categorias são públicos. Comentários exigem login. Os botões de criação, edição e exclusão de posts aparecem para quem possui a permissão correspondente do Django. Conceda essas permissões somente a editores de confiança, pois o enunciado requer renderização do HTML do post.

## Rodar no Windows

No PowerShell, dentro do repositório, com Python 3.12 ou posterior:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Acesse http://127.0.0.1:8000/ e entre com a conta criada. A área de administração está em `/admin/`. Os usuários fictícios de demonstração são autores dos comentários iniciais. Eles não precisam de senhas para a demonstração pública.

Se usar o `db.sqlite3` entregue separadamente, copie o arquivo para a raiz antes de migrar. O banco de entrega não inclui nenhuma credencial utilizável. Crie um superusuário com um nome novo para editar os dados.

## Histórico exigido

```text
ep2-crud-v1   views funcionais sem forms ou validação
ep2-crud-v2   views funcionais com ModelForm
ep2-crud-v3   cinco views genéricas
ep2-comments  ponta do branch comments
ep2-categories ponta do branch categories
```

Os dois branches foram integrados com commits de merge. Use `git log --graph --oneline --all` e `git show ep2-crud-v1:blog/views.py` para inspecionar o histórico. Se recebeu o bundle, clone com `git clone carneiro_crud.bundle carneiro-crud` e crie os branches locais com `git branch comments origin/comments` e `git branch categories origin/categories` antes de trocar o remoto.

## Testes e consultas

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe sql\consultar.py
```

As consultas estão em `sql/` e também podem ser executadas individualmente no DB Browser for SQLite. O arquivo SQLite permanece fora do Git conforme o enunciado.

## GitHub e Render

Crie um repositório vazio no GitHub. Na cópia clonada do bundle, troque o remoto por `git remote set-url origin URL_DO_REPOSITORIO`, depois envie `git push -u origin main comments categories` e `git push origin --tags`.

No Render, crie um **Blueprint** apontando para o repositório e selecione o plano gratuito. O `render.yaml` configura instalação, migrações, dados de demonstração, arquivos estáticos e Gunicorn. A chave secreta é gerada pelo Render. Para testar edição na implantação, defina `DJANGO_SUPERUSER_USERNAME` e `DJANGO_SUPERUSER_PASSWORD` nas variáveis de ambiente antes de implantar. Não coloque credenciais no Git. Reimplante se as variáveis forem incluídas depois da primeira publicação.

O SQLite do serviço gratuito é efêmero. A implantação contém os dados de demonstração. Mudanças feitas no site podem ser perdidas em reinícios ou reimplantações. Para uso persistente, configure um disco do Render em um plano pago e aponte `DJANGO_SQLITE_PATH` para um arquivo nesse disco, executando migrações e carga inicial no início do serviço. O arquivo entregue ao Moodle é o SQLite local, separado da hospedagem.

Inclua os links do GitHub e do Render no relatório ou nos comentários da entrega do Moodle.
