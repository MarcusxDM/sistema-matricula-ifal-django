# sistema-matricula-ifal-django
Aplicação Web de gerência de matrículas para instituições da educação.

## Funcionalidades:
- Cadastro de pessoas: aluno, professor e coordenador de curso
- Matrícula de alunos em determinado curso
- Matrícula de alunos em matérias
- Vincular professor a disciplina
- Cadastro de Períodos
- Cadastro de Atividades
- Cadastro de Notas
- Lista de Presença de Alunos

## Tecnologias:
Back-end: 
- Python
- Django

Banco de Dados: 
- MySQL

Front-end:
- HTML5
- CSS
- Javascript
- Bootstrap 5

Prototipagem:
- Figma

## Dockerização:
- Marcus Pestana
- Karla Araújo


## Configuração e execução da aplicação

### 1. Criar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
```

### 2. Subir os containers (ou executar Dev Container presente no Projeto)

Execute o comando:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Isso irá:

* Construir a imagem da aplicação (`web`)
* Subir o container do banco de dados (`db`)
* Aguardar o banco ficar pronto antes de iniciar a aplicação Django

### 3. Acessar a aplicação

Abra o navegador e acesse:

```
http://localhost:8000
```

### 4. Entrar no container da aplicação web

Caso precise executar comandos Django dentro do container:

```bash
docker-compose -f docker-compose.dev.yml exec web sh
# ou bash se estiver disponível
```

### 5. Executar comandos Django

Dentro do container `web` você pode rodar:

```bash
python manage.py migrate          # Aplica as migrations
python manage.py createsuperuser  # Cria um superusuário
python manage.py runserver 0.0.0.0:8000  # Roda o servidor de desenvolvimento
```

### 6. Parar os containers

Quando não precisar mais da aplicação rodando:

```bash
docker-compose -f docker-compose.dev.yml down
```