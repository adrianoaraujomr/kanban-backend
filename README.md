## Comandos

```
$ alembic upgrade head // inicia banco de dados
$ flask --app src/main --debug run // rodar projeto
```

## Configuração inicial

- Criar um virtualenv
- Usar o virtual env para instalar as dependências necessárias (`pip install flask`)
- Desta forma os pacotes do python ficaram disponivel so neste ambiente

## Criar Projeto

- Criar o arquivo principal, onde a aplicação será instanciada (`main.py`)
- O arquivo principal já basta para a aplicação funcionar, em seguida as rotas podem ser definidas
  - As rotas tbm podem ser diretamente setadas na main
  - Blueprint, criar um arquivo com a blueprint e suas rotas (`routes/*.py`) e registrar a blueprint na main (`main.py`)

## Environment Variables

- Instalar dependecias (`pip install python-dotenv`)
- Criar arquivo env (`.env`)

## Conexão com Banco de Dados

- Instalar dependencias (`pip install sqlalchemy pg8000`)
- `sqlalchemy` para ORM e `pg8000` driver do banco usado
- Criar um arquivo para conectar ao banco (`database.py`)
  - Também pode ser feito no arquivo principal (`main.py`)

## Migrations [[1]](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

- Adicionar a biblioteca de migrations ao projeto (`pip install alembic`)
- Iniciar o alembic para criar a pasta de migrations (`alembic init migrations`)
- Configurar o alembic
  - Configurar url do banco (`alembic.ini`)
  - Criar uma classe base (`models/base.py`)
  - Essa classe base sera extendida por modelos (`models/*.py`)
  - Essa classe também deve ser referenciada em (`migrations/env.py`)
- Criar migrations
  - Automaticamente (`alembic revision --autogenerate -m [message]`)
  - Manualmente (`alembic revision -m [message]`)
- Commitar mudança no banco (`alembic upgrade head`)

## Authentication [[2]](https://www.freecodecamp.org/news/jwt-authentication-in-flask/)

- JWT Authentication
- Instalar dependencias `pip install flask-bcrypt Flask-JWT-Extended`
- Instanciar jwt e setar as chaves `main.py`
- Adicionar annotation a rotas que devem ser protegidas `@jwt_required`
- Criar rota de login `api/usuario/usuarioRoute.py`
  - Essa rota vai comparar a senha enviada com a salva no banco (salva como hash, para questão de segurança)
  - Se o login houver sucesso retorna um token

## Authorization

## Testes (\*)

## Docker

## CI/CD

# Refs

[1] - https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a
[2] - https://www.freecodecamp.org/news/jwt-authentication-in-flask/
