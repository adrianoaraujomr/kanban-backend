# Rodar projeto

### Pré requisitos

- Python estar instalado
- Preencher valores do `.env.example` e renomea-lo para `.env`
- Banco de dados estar rodando de acordo com valores do `.env`

- Obs.: No arquivo infra.yml já possui a configuração de como rodar o banco como docker com os valores presentes em `.env`

```
$ docker compose -f infra.yml up
```

- Obs.: Rodando o compose da seguinte forma é util para desenvolvimento já que o comando `docker compose up` vai também subir um docker da própria aplicação

### Comandos

```
$ pyenv activate [nome env]        # (opcional) apenas se tiver pyenv instalado e configurado
$ pip install -r requirements.txt  # so precisa ser feito a primeira vez que rodar o projeto (instala dependencias)
$ alembic upgrade head             # rodas as migrations, quando alterar migrations esse comando deve ser rodado
$ flask --app src/main --debug run # inicia a aplicação
```

# Criar Projeto do Zero

## Flask

### Instanciar aplicação e definir endpoints

- Criar o arquivo principal, onde a aplicação será instanciada (`main.py`) [[1]](https://flask.palletsprojects.com/en/stable/quickstart/)
  - Obs.: O arquivo principal já basta para a aplicação funcionar
- Em seguida as rotas/endpoints devem ser criados
  - Existem várias abordagens de se criar, a mais simples é criar diretamente na main usando a aplicação criada como anotação `@app.route()`
  - Outra abordagem é fazer o uso de Blueprint [[2]](https://flask.palletsprojects.com/en/stable/blueprints/)
    - instanciar Blueprint `bp = Blueprint()` (`api/**/**_route.py`)
    - assim como anteriormente usar uma anotation para definir o endpoint `@bp.route()`
    - registrar a blueprint no app `app.register_blueprint(bp, "/bp")` (`main.py`)

## Geral

### Environment Variables

- Instalar a lib (`pip install python-dotenv`)
- Criar arquivo env (`.env`)
- Obs.: Arquivos `.env` não devem ser commitados diretamente por possuirem dados sensíveis, logo deve se adicionar esse arquivo no `.gitignore`. Também é bom criar um arquivo `.env.example` que deixa claro quais váriaveis de ambiente o projeto necesseta. O que facilita algume roda-lo pela primeira vez.
  **TBD: Aspas ou não Aspas**

### Banco de dados

#### SQL

##### ORM e Conectar no banco de dados

- Escolher um ORM. Facilita comunicção com o BD. Middleware entre Classes e BD. (ex.: `sqlalchemy`)
- Escolher um banco de dados e instalar o lib de coumunicação do banco (ex.: `pg8000`)
  - Instalar dependências `pip install sqlalchemy pg8000`
- SqlAlchemy [[33]](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
  - Definir modelos, criar classes python e mapear as tabelas do banco para essas classes (`/models/*.py`) [[34]](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)
  - Criar uma engine, ela vai ser a responsável por criar conexões com o banco de dados (`/database.py`) [[35]](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
    - A engine disponibiliza `connection`, que é usada para executar instruções SQL
    - Usando a engine e `Sessions`, é possivel fazer o mesmo que com `connection`, que é um versão mais nova [[36]](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-executing-orm-session)

##### Migrations

- Migrations é uma forma de controlar o versionamento do esquema de banco de dados [[3]](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)
- Escolher uma biblioteca para lidar com as migrations (ex.: `alembic`) [[37]](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
  - Instalar dependência `pip install alembic`
  - Iniciar o ambiente alembic `alembic init migrations` (Obs.: migrations é apenas o nome que vai ser dado ao diretorio do alembic, no tutorial é `alembic init alembic`)
  - Configurar URL do banco, se depende de `.env` definir em `migrations/env.py`, se url estática `alembic.ini` em `sqlalchemy.url`
  - Criar uma classe base para os modelos (`models/base.py`) que extende `DeclarativeBase`
  - A classe base sera para outros modelos (`models/*.py`)
  - Essa classe também deve ser referenciada em `migrations/env.py` para dar valor ao `target_metadata`
  - Em `migrations/env.py` o `config.set_main_option("sqlalchemy.url", "")` seta o valor da url do banco, podendo fazer uso de envs
- Comandos para migrations
  - Migration automatica (`alembic revision --autogenerate -m [message]`)
  - Migration Manualm (`alembic revision -m [message]`)
  - Commitar mudança no banco (`alembic upgrade head`)

#### NoSQL

- TBD

### Authentication

- Mecanismo de segurança da API [[4]](https://www.freecodecamp.org/news/jwt-authentication-in-flask/)

#### JWT Authentication

- Forma de autenticação stateless, servidor envia para o cliente um token com informações do usuário [[21]](https://medium.com/@rohitraj1912000/demystifying-authentication-and-authorization-in-backend-systems-52489c3fae8c)
- Cliente usa esse token na requisição para obter recursos do servidor
- Instalar dependencias `pip install flask-bcrypt Flask-JWT-Extended`
- Instanciar jwt e setar as chaves `main.py`
- Adicionar annotation a rotas que devem ser protegidas `@jwt_required`
- Criar rota de login `api/usuario/usuarioRoute.py`
  - Essa rota vai comparar a senha enviada com a salva no banco (salva como hash, para questão de segurança)
  - Se o login houver sucesso retorna um token

#### Session Tokens [[21]](https://medium.com/@rohitraj1912000/demystifying-authentication-and-authorization-in-backend-systems-52489c3fae8c)

- Gerados a partir de uma autenticação bem suceidada e armazenada no servidor
- Token é associado a uma sessão do cliente (session ID armazenada em coockie)

### Authorization [[22]](https://frontegg.com/guides/authorization-a-complete-guide#:~:text=Implement%20Authorization%20Policies&text=You%20can%20use%20various%20types,discretionary%20access%20control%20(DAC).)

#### Role-Based Access Control (RBAC) [[23]](https://www.redhat.com/en/topics/security/what-is-role-based-access-control)

- Usuários acessam recursos de acordo com uma role
- Role define quais ações/recursos podem ser realizadas/acessados
- Usuários possuem uma ou mais roles
- Cada role possui certas permissões
- Usuário ganha permissões de acordo com as roles designadas

##### Implementação [[25]](https://blog.stackademic.com/implementing-role-based-access-control-rbac-in-flask-f7e69db698f6)

- Criar as roles `src/models/role.py`
- No caso de tabela criar o relacionamento dela com a tabela de Usuário `src/models/user.py`
  - Criar a tabela intermediária entre role e usuario `user_roles`
  - Adicionar no Usuário um atributo que lista suas roles `User.roles`
- Criar decorator para filtrar recursos de acordo com role `src/decorators/auth.py`
- Obs.: Decorators são um padrão de programação usados para adicionar funcionalidades a funções sem alterar suas estruturas [[26]](https://www.datacamp.com/tutorial/decorators-python)

#### Attribute-Based Access Control (ABAC)

- TODO

### Tratamento de erros [[27]](https://dev.to/ctrlaltvictoria/backend-error-handling-practical-tips-from-a-startup-cto-h6)

#### Geral

- Importante para debug, resiliência, segurança e experiência do usuário
- Centralized Error handling
  - Facilita a leitura e manutenção do código
  - Pode ser feito atráves de middleware
- Custom Error Classes
  - Divide erros em tipos customizáveis
  - Error handling middleware pode ser comportar diferente dependendo do tipo do erro
- Try/catch
  - Básico do tratamento de erros
  - É recomendadável tratar apenas erros conhecidos, deixando os desconhecidos para o error handling global

#### Python [[28]](https://docs.python.org/3/tutorial/errors.html)

- Exceptions
- Erros detectados durante execução
- Uma execção resulta em uma mensagem de erro quando não tratada
- Handling Exceptions
  - Código dentro de um `try` é executado mas se ocorre uma exceção que bate com o tipo no `exception` o bloco dele é executado
  - `BaseException` é a classe base para todas as exceções
  - `Exception` um subclasse de `BaseException` é a base para todas exceções não fatais
- User-defined Exceptions
  - Criadas a partir de classes geralmente extendendo `Exception` (direto ou indiretamente)
  - Geralmente são simples e possuem atributos que permite inofrmações sobre o erro serem extraidas
  - Por convenção podem terminar com o nome `Error`

#### Flask [[29]](https://flask.palletsprojects.com/en/stable/errorhandling/)

- O Flask por padrão já tem uma forma de lidar com exceções
- Se uma execção não é tratada ele devolve uma página padrão com erro 500
- É possível criar funções para lidar customizar como a mensagem de erro é enviada
  - `app.register_error_handler(400, handle_bad_request)`: A função `handle_bad_request` trata o retorno quando ocorre um erro 400
  - `app.register_error_handler(werkzeug.exceptions.HTTPException, handle_exception)`: Dessa forma é possível criar um retorno padrão para qualquer exceção HTTP
- Para criar classes expecificas de erros HTTP, basta extender `werkzeug.exceptions.HTTPException`, e adicionar os atributos `code` e `description` (ex.: `global_error_handling.py`)
- Com um handler global e classes de erros HTTP é possível retornar mensagens que facilitam compreender que erro ocorreu

### Logging [[30]](https://flask.palletsprojects.com/en/stable/logging/)

- Flask faz uso do logger padrão do python `logging`
- Fazer uso do sistema padrão do python tem a vantagem de integrar seus logs com logs de bibliotecas
- Níveis de logging [[31]](https://docs.python.org/3/library/logging.html)
  - NOTSET (0): busca valor do log antecessor, senão todos eventos são logados
  - DEBUG (10): informação detalhada (ambiente de desenvolvimento)
  - INFO (20): confirma que tudo está funcionando como esperado
  - WARNING (30): indicação de algo inesperado, ou que algo irá falhar no futuro
  - ERROR (40): devido um erro algo não foi executado
  - CRITICAL (50): um erro sério que pode levar a parada de execução do programa
- É necessário configurar o logging no projeto antes de acessar `app.logging` senão uma configuração padrão será usada
- A configuração é feita atráves do método `dictConfig` [[32]](https://betterstack.com/community/guides/logging/how-to-start-logging-with-flask/)
  - `formatters`: define o padrão de formatação do log
  - `handlers`: envia logs para diversos destinos
  - `root`: define as configuração do log de `root`

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

(https://docs.docker.com/compose/how-tos/multiple-compose-files/) Multiplos compsoe

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
[[21] https://medium.com/@rohitraj1912000/demystifying-authentication-and-authorization-in-backend-systems-52489c3fae8c](https://medium.com/@rohitraj1912000/demystifying-authentication-and-authorization-in-backend-systems-52489c3fae8c)  
[[22] https://frontegg.com/guides/authorization-a-complete-guide#:~:text=Implement%20Authorization%20Policies&text=You%20can%20use%20various%20types,discretionary%20access%20control%20(DAC).](<https://frontegg.com/guides/authorization-a-complete-guide#:~:text=Implement%20Authorization%20Policies&text=You%20can%20use%20various%20types,discretionary%20access%20control%20(DAC).>)  
[[23] https://www.redhat.com/en/topics/security/what-is-role-based-access-control](https://www.redhat.com/en/topics/security/what-is-role-based-access-control)  
[[24] https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)  
[[25] https://blog.stackademic.com/implementing-role-based-access-control-rbac-in-flask-f7e69db698f6](https://blog.stackademic.com/implementing-role-based-access-control-rbac-in-flask-f7e69db698f6)  
[[26] https://www.datacamp.com/tutorial/decorators-python](https://www.datacamp.com/tutorial/decorators-python)  
[[27]](https://dev.to/ctrlaltvictoria/backend-error-handling-practical-tips-from-a-startup-cto-h6)  
[[28]](https://docs.python.org/3/tutorial/errors.html)  
[[29]](https://flask.palletsprojects.com/en/stable/errorhandling/)  
[[30]](https://flask.palletsprojects.com/en/stable/logging/)  
[[31]](https://docs.python.org/3/library/logging.html)  
[[32]](https://betterstack.com/community/guides/logging/how-to-start-logging-with-flask/)  
[[33]](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)  
[[34]](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)  
[[35]](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)  
[[36]](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-executing-orm-session)  
[[37]](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
