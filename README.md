## Rodar projeto

### Pré requisitos

- Python estar instalado
- Instalar os pacotes contidos no `requirements.txt` (`pip install flask` [Obs.: se fazer uso do pyenv ativar o env antes de rodar, senão primeiro comando não é necessário])
- Preencher valores do `.env.example` e renomea-lo para `.env`
- Banco de dados estar rodando de acordo com valores do `.env`

### Comandos

```
$ pyenv activate [nome env]
$ alembic upgrade head
$ flask --app src/main --debug run
```

## Como Criar Projeto do Zero

- Criar o arquivo principal, onde a aplicação será instanciada (`main.py`) [[1]](https://flask.palletsprojects.com/en/stable/quickstart/)
- O arquivo principal já basta para a aplicação funcionar, em seguida as rotas podem ser definidas
  - As rotas tbm podem ser diretamente setadas na main
  - Blueprint, criar um arquivo com a blueprint e suas rotas (`routes/*.py`) e registrar a blueprint na main (`main.py`) [[2]](https://flask.palletsprojects.com/en/stable/blueprints/)

### Environment Variables

- Instalar dependecias (`pip install python-dotenv`)
- Criar arquivo env (`.env`)

### Conexão com Banco de Dados

- Instalar dependencias (`pip install sqlalchemy pg8000`)
- `sqlalchemy` para ORM e `pg8000` driver do banco usado
- Criar um arquivo para conectar ao banco (`database.py`)
  - Também pode ser feito no arquivo principal (`main.py`)

### Migrations [[3]](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

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

### Authentication [[4]](https://www.freecodecamp.org/news/jwt-authentication-in-flask/)

- JWT Authentication
- Instalar dependencias `pip install flask-bcrypt Flask-JWT-Extended`
- Instanciar jwt e setar as chaves `main.py`
- Adicionar annotation a rotas que devem ser protegidas `@jwt_required`
- Criar rota de login `api/usuario/usuarioRoute.py`
  - Essa rota vai comparar a senha enviada com a salva no banco (salva como hash, para questão de segurança)
  - Se o login houver sucesso retorna um token

### Authorization

### Testes (\*)

### Docker

### CI/CD

# Refs

[[1] https://flask.palletsprojects.com/en/stable/quickstart/](https://flask.palletsprojects.com/en/stable/quickstart/)  
[[2] https://flask.palletsprojects.com/en/stable/blueprints/](https://flask.palletsprojects.com/en/stable/blueprints/)  
[[3] https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)  
[[4] https://www.freecodecamp.org/news/jwt-authentication-in-flask/](https://www.freecodecamp.org/news/jwt-authentication-in-flask/)
