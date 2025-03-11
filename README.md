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

### Authorization (TBD)

### Testes [[5]](https://flask.palletsprojects.com/en/stable/testing/)[[6]](https://www.digitalocean.com/community/tutorials/unit-test-in-flask)[[7]](https://www.digitalocean.com/community/tutorials/unit-test-in-flask)[[10]](https://testdriven.io/blog/flask-pytest/)

- Adicionar a biblioteca pytest ao projeto (`pip install pytest`)
- Em seguida é criado um diretório em que os testes serão armazenados (`/test`)
- O pytest irá buscar e rodar todos os arquivos no seguinte formatos (`test_*.py`, `*_test.py`)
- Para rodar todos os testes basta usar o comando `pytest`
- Criar um novo arquivo `.env` para as variaveis de teste [[9]](https://pytest-with-eric.com/pytest-best-practices/pytest-environment-variables/)
- O arquivos `/test/conftest.py` define as fixtures, que serão pedaçõs de código que o pytest rodara automaticamente
  - Ou seja ao fazer a configuração da aplicação no `conftest.py` o pytest cuidara de tudo automaticamente

#### Banco de dados

- Em mémoria (SQLite)
- Banco de teste
  - Criar e destruir para cada grupo de teste (`@pytest.fixture` com o uso de `Base.metada.create_all`)
  - Limpar banco de dados para cada grupo de teste (`@pytest.fixture` com o uso de `Base.metada.drop_all`, `scope` da fixture define se esse grupo vai ser classes ou métodos)
  - Definir um novo valor para as variáveis de banco do `.env`

#### Mocking (TBD)

- Codigo criado para substituir servicos de terceiros, requisições na hora de testar

#### Unit tests [[6]](https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing)[[8]](https://www.ramotion.com/blog/what-is-backend-testing/#:~:text=Backend%20testing%20involves%20testing%20these,other%20systems%2C%20and%20server%20configurations.)

- Testam, metodos, classes e compenentes
- Devem ser leves
- Testes de lógica de código
- Ex.: `test/test_unit.py`

#### Integration tests [[6]](https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing)[[8]](https://www.ramotion.com/blog/what-is-backend-testing/#:~:text=Backend%20testing%20involves%20testing%20these,other%20systems%2C%20and%20server%20configurations.)

- Verifica se a conexão de diferentes componentes da aplicação funcionam
- Por exemplo, integração com o banco de dados
- Microserviços funcioname como esperado

#### Functional tests [[6]](https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing)[[8]](https://www.ramotion.com/blog/what-is-backend-testing/#:~:text=Backend%20testing%20involves%20testing%20these,other%20systems%2C%20and%20server%20configurations.)

- Um superset do integration
- Por exemplo, além de verificar a conexão com o banco de dados verificar se uma query funciona como esperado
- Ex.: `test/test_login.py`

#### End to End tests [[6]](https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing)[[8]](https://www.ramotion.com/blog/what-is-backend-testing/#:~:text=Backend%20testing%20involves%20testing%20these,other%20systems%2C%20and%20server%20configurations.)

- Muito caros
- Replica o comportamento de um usuário com todo o ambiente da aplicação

### Docker (TBD)

### CI/CD (TBD)

# Refs

[[1] https://flask.palletsprojects.com/en/stable/quickstart/](https://flask.palletsprojects.com/en/stable/quickstart/)  
[[2] https://flask.palletsprojects.com/en/stable/blueprints/](https://flask.palletsprojects.com/en/stable/blueprints/)  
[[3] https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)  
[[4] https://www.freecodecamp.org/news/jwt-authentication-in-flask/](https://www.freecodecamp.org/news/jwt-authentication-in-flask/)  
[[5] https://flask.palletsprojects.com/en/stable/testing/](https://flask.palletsprojects.com/en/stable/testing/)  
[[6] https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing](https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing)  
[[7] https://www.digitalocean.com/community/tutorials/unit-test-in-flask](https://www.digitalocean.com/community/tutorials/unit-test-in-flask)  
[[8] https://www.ramotion.com/blog/what-is-backend-testing/#:~:text=Backend%20testing%20involves%20testing%20these,other%20systems%2C%20and%20server%20configurations.](https://www.ramotion.com/blog/what-is-backend-testing/#:~:text=Backend%20testing%20involves%20testing%20these,other%20systems%2C%20and%20server%20configurations.)  
[[9] https://pytest-with-eric.com/pytest-best-practices/pytest-environment-variables/](https://pytest-with-eric.com/pytest-best-practices/pytest-environment-variables/)
[[10] https://testdriven.io/blog/flask-pytest/](https://testdriven.io/blog/flask-pytest/)
