# Arquitetura do Sistema — go_notify

## 1. Objetivo do Sistema

O **go_notify** é uma API desenvolvida em **Python** com **FastAPI** que tem como objetivo central a **notificação e comunicação**, expondo também recursos de gerenciamento de usuários, produtos, sessões (autenticação) e integração com um serviço de **Chat com IA**.

O nome do projeto (`go_notify`) indica que a aplicação nasceu com foco em **notificações**, evoluindo para uma API mais ampla que também atende:

- Autenticação e emissão de tokens (JWT).
- Gestão de sessões persistidas no banco.
- CRUD de usuários e produtos (com reviews aninhadas).
- Integração com serviço externo de chat com IA.
- Preparação (ainda incompleta) para comunicação em tempo real via WebSocket.

A API funciona como **backend** consumido por clientes externos (frontend/outros serviços), seguindo o padrão REST com respostas padronizadas em JSON.

---

## 2. Visão Geral da Arquitetura

A aplicação segue uma arquitetura **em camadas** (estilo "MVC adaptado"), organizada nos seguintes pacotes:

| Camada | Diretório | Responsabilidade |
|---|---|---|
| Rotas / Views | `app/views/` | Definição dos endpoints HTTP (FastAPI routers) |
| Controllers | `app/controllers/` | Regras de orquestração e acesso a dados (CRUD) |
| Models / DTOs | `app/db/models/` e `app/dtos/` | Modelos de dados Pydantic (persistência e transferência) |
| Services | `app/services/` | Integrações externas (chat com IA) e regras de negócio |
| Auth | `app/auth/` | Autenticação, tokens JWT e validação de sessão |
| DB | `app/db/` | Conexão com o banco de dados (MongoDB) |
| Util | `app/util/` | Configuração, cliente HTTP e tratamento de exceções |
| Socket | `app/socket/` | Comunicação em tempo real (esboço) |

### Fluxo típico de uma requisição

```
Client HTTP
    │
    ▼
nginx (load balancer, opcional)
    │
    ▼
FastAPI Router (app/views/*)
    │
    ▼
ApplicationManager (singleton) ──► Controller (app/controllers/*)
    │                                    │
    │                                    ▼
    └── DTO (Pydantic) ──► MongoDB (via PyMongo)
```

### Stack Tecnológica

- **Linguagem:** Python 3.13
- **Framework Web:** FastAPI 0.113 + Uvicorn
- **Banco de Dados:** MongoDB (PyMongo + MongoEngine)
- **Validação/Serialização:** Pydantic v2
- **Autenticação:** JWT (PyJWT) + Bcrypt (passlib)
- **Comunicação em tempo real:** python-socketio (esboço)
- **Integração HTTP:** requests
- **Infraestrutura:** Docker + Docker Compose, NGINX (load balancer)
- **Testes:** pytest, pytest-cov, mongomock, pytest-asyncio

---

## 3. Componentes em Detalhe

### 3.1. `ApplicationManager` (Singleton)

Gerencia a criação e o **reuso de instâncias de controllers**, evitando múltiplas instâncias desnecessárias:

```python
class ApplicationManager:
    _instance = None
    def __new__(cls): ...
    def get(controller, client=None): ...
    def create_instance(...): ...
```

- Implementa o padrão **Singleton**.
- Faz cache de controllers por `collection_name`.
- Permite injetar um client MongoDB alternativo (usado nos testes com `mongomock`).

### 3.2. Camada de Controllers (`app/controllers/`)

Há um `BaseController[T]` **genérico** que concentra todo o CRUD:

- `create`, `update`, `get_filter`, `get_by_id`, `get_with_query`, `get_all`, `remove`.
- Os controllers específicos (`UserController`, `ProductController`, `SessionController`) apenas herdam e definem o `collection_name` e o DTO.

Isso reduz drasticamente a duplicação de código de persistência.

### 3.3. Camada de DTOs (`app/dtos/` e `app/db/models/`)

- `BaseDTO` / `DTO` estendem o `BaseModel` do Pydantic.
- `DTO` já inclui campos comuns de auditoria: `id` (`_id` do Mongo), `created_at`, `updated_at`, `updated_by`, `created_by`.
- `CustomObjectId` permite converter strings ↔ `ObjectId` de forma transparente.
- Há DTOs separados para **resposta** (`ResponseDTO`, `ResponseModelDTO`), **entrada** (`CreateProductDTO`, `EditProductDTO`, etc.) e **persistência** (`ProductDTO`, `UserDTO`, `SessionDTO`).

### 3.4. Autenticação e Sessão (`app/auth/`)

- `create_access_token` gera JWT com `exp`.
- `get_password_hash` / `verify_password` usam bcrypt.
- `get_token` e `ValidateToken` validam:
  - Se o header `Authorization` existe.
  - Se a sessão **não expirou**, consultando a collection `session` no MongoDB.
- `/session/login` usa `OAuth2PasswordRequestForm` e persiste a sessão no banco.

### 3.5. Integração com Serviço Externo (`app/services/`)

- `ChatAIService` encapsula chamadas HTTP a uma API externa de chat (URL vinda de `CHAT_API_URL`).
- `app/util/request.py` (`Request`) é um wrapper simples sobre `requests`.

### 3.6. Infraestrutura

- **Dockerfile:** imagem `python:3.13.1-alpine`.
- **docker-compose:** sobe MongoDB, duas réplicas da aplicação e NGINX.
- **nginx.conf:** load balancer entre `go-notify-local1` (porta 8008) e `go-notify-local2` (porta 8007), escutando em 8001.

---

## 4. Pontos Fortes

1. **Separação em camadas** bem definida (views, controllers, services, DTOs), o que facilita a manutenção e a evolução.

2. **`BaseController` genérico com CRUD reutilizável** — elimina repetição de código de persistência e acelera a criação de novos recursos.

3. **Uso do Pydantic v2** para validação, serialização e tipagem robusta dos dados, incluindo suporte a `ObjectId` do MongoDB via `CustomObjectId`.

4. **`ApplicationManager` (Singleton)** centraliza e reutiliza instâncias de controllers, reduzindo acoplamento e custo de instanciação.

5. **Campos de auditoria padronizados** na classe `DTO` (`created_at`, `updated_at`, `created_by`, `updated_by`).

6. **Autenticação real** com JWT, hash de senha (bcrypt) e controle de expiração de sessão persistido no banco.

7. **Respostas padronizadas** (`ResponseDTO` / `ResponseModelDTO`), garantindo consistência no formato de saída da API.

8. **Testabilidade razoável** — o `ApplicationManager` aceita injeção de client Mongo, permitindo usar `mongomock` nos testes.

9. **Prontidão para deploy** com Docker, Docker Compose e load balancer (NGINX), incluindo múltiplas réplicas.

10. **Injeção de dependência** do FastAPI (`Depends`) utilizada nos routers para validação de token.

11. **Tratamento global de exceções** customizado (`midle_erros`) que normaliza erros para o padrão de resposta da API.

---

## 5. Pontos Fracos

1. **Segredos hardcoded no código-fonte:**
   - Credenciais do PostgreSQL fixas em `compose/postgres.yaml`.

2. **Falta de variáveis de ambiente para configuração sensível:** a chave JWT deveria vir de variável de ambiente/secret manager, nunca versionada.

3. **Inconsistência no acesso a dados:**
   - `requirements.txt` inclui **dois** drivers/ODMs: `mongoengine` e PyMongo.
   - `app/db/models/*` importa `mongoengine` mas o código real de persistência usa PyMongo (`MongoClient`). Isso gera confusão e dependência desnecessária.

4. **Código de exemplo/"morto" em produção:**
   - `app/auth/session.py` (`ManagerSession`) parece redundante e não é integrado ao fluxo real.
   - `validations/bot.py` é um script de análise de criptomoedas fora do escopo da API.

5. **Duplicação de nomes de funções nas rotas:**
   - Em `app/views/user.py`, várias funções chamam-se `read_system_status`, o que reduz legibilidade e dificulta rastreamento.

6. **Falta de tratamento de exceções específicas:**
   - `BaseController` lança `NotFoundAPI`, mas `session_expired` e outros fluxos podem quebrar com `None`.
   - O handler global assume a existência de atributos (`exc.message`, `exc.status_code`) que nem toda exceção possui.

7. **Arquitetura de sessão frágil:**
   - A validação do token consulta o banco a cada requisição; a lógica de expiração está espalhada entre `ValidateToken` e `session_expired`.
   - `ValidateToken` definido como `Protocol` não é idiomático para dependência FastAPI.

8. **Injeção de dependência manual via Singleton:**
   - O `ApplicationManager` é um Singleton global, o que acopla o código e dificulta testes e inversão de controle (IoC) real.

9. **CORS e middlewares configurados de forma dispersa** — `add_middleware` é chamado em `app/__init__.py` depois de importar routers, gerando ordem frágil de inicialização.

10. **Estrutura de erros incompleta:**
    - `app/util/exception.py` define um `NewTestAPI` com status HTTP 450 (não padrão).
    - Há importação entre módulos sujeita a ciclos (ex.: `app.views.erros` importa `app`).

11. **Pouca cobertura de testes:**
    - Testes concentram-se em `SessionController` e `ApplicationManager`.
    - Não há testes de rotas (FastAPI `TestClient`), nem de `ProductController`, `UserController` ou do serviço de chat.

12. **Sem camada de validação/negócio separada:**
    - Regras de negócio (montar o hash, popular reviews) estão dentro das **views**, o que fere a separação de responsabilidades.

13. **Arquivos auxiliares como `debug.py` e `main.py`** duplicam o bootstrap do servidor, e `main.py` importa `app` de forma indireta.

---

## 6. O Que Pode Ser Melhorado (Melhores Práticas)

### 6.1. Segurança

- **Mover `SECRET_KEY` e credenciais para variáveis de ambiente**, usando biblioteca como `pydantic-settings` para carregar e validar configuração.
- **Remover segredos hardcoded** (`"jessica"`, `"fake-super-secret-token"`) e credenciais de banco versionadas.
- **Usar força de hash adequada e rotação de chave**, além de `SecretStr` para não expor senhas em logs.
- **Validação de token 100% via JWT** (assinatura + `exp`) em vez de consultar o banco a cada requisição; persistir sessão só se houver requisito de revogação.
- **Configurar HTTPS**, `secure` nos cookies e revisar `allow_credentials=True` no CORS.

### 6.2. Arquitetura e Organização

- **Padronizar o acesso a dados:** escolher um único driver/ODM (recomenda-se **PyMongo** puro ou um ODM coerente). Remover `mongoengine` se não for usado.
- **Introduzir uma camada de serviço** para regras de negócio (ex.: criação de usuário com hash, adição de reviews, expiração de sessão), deixando as views apenas como roteadores finos.
- **Separar a criação da aplicação FastAPI** numa factory (`create_app()`) com organização clara de middlewares, rotas e handlers.
- **Adotar inversão de controle** com o sistema de dependências do FastAPI (`Depends`) para controllers, em vez de Singleton manual.
- **Renomear as funções das views** para nomes descritivos e únicos (`create_user`, `get_user_by_email`, etc.).

### 6.3. Qualidade de Código e Padrões

- **Melhorar o tratamento de exceções** com classes de erro consistentes (herdando de `HTTPException` ou um handler que trate `IExceptionAPI` corretamente).
- **Type hints consistentes**: não deve haver `tuple` ou `None` inesperados; `authenticate_user` pode retornar `DTO | bool`, o que é confuso — melhor retornar `DTO | None` e lançar erro na camada superior.
- **Ativar linters e formatadores** (`ruff`, `black`, `isort`, `mypy`) para manter consistência.
- **Padronizar respostas e status HTTP**: usar corretamente `201`, `204`, `404`, `401`, `422`, em vez de status não padrão.

### 6.4. Testes

- **Expandir a suíte de testes** para:
  - Rotas via `TestClient` (testes de integração).
  - `ProductController` e `UserController`.
  - `ChatAIService` com mock da API externa.
  - Handler global de erros.
- **Usar fixtures e `pytest`** de forma mais sistemática, isolando dados entre testes.
- **Medir cobertura** continuamente no pipeline de CI.

### 6.5. Observabilidade e Manutenibilidade

- **Adicionar logging estruturado** (substituir os vários `print(...)` em `config.py` e views por `logging`).
- **Adicionar monitoramento de saúde** (`/health`, `/readiness`) e métricas.
- **Versionar as rotas** (`/api/v1/...`) para permitir evolução sem quebrar clientes.
- **Documentar a API** com OpenAPI (aproveitar o já gerado pelo FastAPI) e `docstrings`.
- **Criar um `Startup`** para inicialização da aplicação (fechamento/limpeza do client Mongo em `shutdown`).

### 6.6. Infraestrutura e CI/CD

- **Automatizar o pipeline** (GitHub Actions/GitLab CI/Jenkins) com build, testes e lint.
- **Remover segredos dos arquivos compose**; usar Docker Secrets ou variáveis de ambiente.
- **Ajustar o Dockerfile** com `CMD` explícito e possível multi-stage para reduzir o tamanho da imagem.
- **Alinhar portas**: o `nginx.conf` referencia portas internas (8007/8008) que podem conflitar; padronizar exposição.
- **Versionar as dependências** com exatidão (há `pandas` sem versão e pacote interno `basic-components-fpp`).

---

## 7. Resumo Executivo

O `go_notify` possui uma **base arquitetural promissora** — com camadas bem definidas, DTOs tipados com Pydantic e um CRUD genérico reutilizável que reduz duplicação. No entanto, para atingir um padrão de produção robusto, precisa evoluir principalmente em:

1. **Segurança** (remover segredos hardcoded e centralizar configuração).
2. **Consistência de dados** (um único driver/ODM).
3. **Separação de responsabilidades** (extrair regras de negócio das views).
4. **Cobertura de testes** (hoje insuficiente).
5. **Limpeza de código morto** e organização de bootstrap.
6. **Observabilidade e padronização de erros/respostas.**

Com esses ajustes, o sistema se tornará mais seguro, escalável e facilmente mantível, alinhado às melhores práticas de desenvolvimento de APIs com FastAPI e MongoDB.