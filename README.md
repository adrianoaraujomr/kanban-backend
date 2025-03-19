# Rodar projeto

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

### Docker [[11]](https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/)

- Criar `Dockerfile`
- Seleciona versão do python (`FROM`)
- Criar um diretório dentro do container para armazenar a aplicação e executar os comandos (`WORKDIR`)
- Copia `requirements.txt` para dentro do container e instala as dependencias (`COPY`)
  - Isso é feito para aproveitar o cache do docker. Se algum arquivo do projeto for mudado os pacotes do requirements não mudam.
  - Obs.: O `COPY` não copia arquivos ocultos
- Em seguida se copia o projeto para o container (`COPY`)
- Usar `EXPOSE` para expor uma porta da container
- Por último é adicionado o comando para rodar a aplicação (`RUN`)

```
$ docker build --tag [nome imagem] . # Monta a imagem
```

#### Docker Compose [[12]](https://blog.teclado.com/run-flask-apps-with-docker-compose/)[[13]](https://docs.docker.com/reference/compose-file/)

- Criar `docker-compose.yml`
- `version`: Escolher a versão do composer
- `services`: Os containers
  - `image`: Imagem usada como base, pode ser mudado para `build: .` para imagens locais.
  - `ports`: Mapeia porta do container, para a máquina. Possibilita acessar por localhost.
  - `depends_on`: Indica que um serviço so será iniciado depois que outro já estiver iniciado.
  - `volumes`: ????
  - `network`: Adiciona o serviço a rede, que possibilita comunicar com outros containers.
  - `enviroment`/`env_file`: Adiciona váriaveis de sistema ao container (arquivos .env não são copiados para o container)
- `networks`: Cria uma rede Docker.
- Para que o alembic execute a migração se adiciona um `command` para que as migrations sejam executas antes de executar a aplicação [[14]](https://stackoverflow.com/questions/68225845/how-to-autogenerate-and-apply-migrations-with-alembic-when-the-database-runs-in)
- Possiveis problemas:
  - DB_HOST, host do db muda ao se containarizar. Geralmente seria localhost, mas na docker network a aplicação acessa pelo nome do serviço `db`
  - Ao inicializar o flask é preciso liberar para aceitar conexões não apenas do localhost (`host=0.0.0.0`). Já que se quiser acessar o container dá máquina esse endereço não é entendido como localhost dentro do container

### CI/CD [[15]](https://www.redhat.com/pt-br/topics/devops/what-is-ci-cd)[[16]](https://github.com/resources/articles/devops/ci-cd)

- Integração contínua (CI)
- Entrega contínua (CD)
- Prática para melhorar o desenvolvimento de software
- Automatização de build, testing e deploy
- DevOps automation
- No GitHub é o GitHub Actions

#### CI (GitHub Actions) [[17]](https://docs.github.com/pt/actions/about-github-actions/understanding-github-actions)

- Build, testa e adiciona automaticamente código a um repositório
- O objetivo desse workflow é impedir um merge no caso de as alterações quebrarem um dos testes
- Criar um novo workflow [[18]](https://docs.github.com/en/actions/writing-workflows/quickstart)
  - Criar a partir de um template no GitHub (Repository -> Actions -> new workflow)
  - Criar um novo arquivo `.yml` em `/.github/workflows`
- Adicionar service do banco de dados [[19]](https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers)
- Váriaveis env [[20]](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables)
  - Possui diferentes níveis: organization, repository e environment
  - Adicionar secrets e variables no repository (Repository -> Settings -> Secrets and variables -> Actions)
  - Para acessar o valor das váriaveis bastar usar `${{ vars.*** }}` e `${{ secrets.*** }}`
- `steps` vai ditar a ordem de execução das atividades do job
  - `name` é o nome do `step`
  - `uses` referência uma ação reutilizavel
  - `run` define comandos a serem rodados
- Steps necessários
  - Instalar dependências
  - Instalar PostgresqlCliente (Objetivo desse passo é usar o cliente para esperar o postgres stanciar)
  - Aguardar o postgres subir
  - Inicializar o banco de dados
  - Testar a aplicação

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
[[11] https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/](https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/)  
[[12] https://blog.teclado.com/run-flask-apps-with-docker-compose/](https://blog.teclado.com/run-flask-apps-with-docker-compose/)  
[[13] https://docs.docker.com/reference/compose-file/](https://docs.docker.com/reference/compose-file/)  
[[14] https://stackoverflow.com/questions/68225845/how-to-autogenerate-and-apply-migrations-with-alembic-when-the-database-runs-in](https://stackoverflow.com/questions/68225845/how-to-autogenerate-and-apply-migrations-with-alembic-when-the-database-runs-in)  
[[15] https://www.redhat.com/pt-br/topics/devops/what-is-ci-cd](https://www.redhat.com/pt-br/topics/devops/what-is-ci-cd)  
[[16] https://github.com/resources/articles/devops/ci-cd](https://github.com/resources/articles/devops/ci-cd)  
[[17] https://docs.github.com/pt/actions/about-github-actions/understanding-github-actions](https://docs.github.com/pt/actions/about-github-actions/understanding-github-actions)  
[[18] https://docs.github.com/en/actions/writing-workflows/quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart)  
[[19] https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers](https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers)  
[[20] https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables)
