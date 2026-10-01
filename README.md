# 📅 AgendaPro

Sistema de agendamento desenvolvido com **Python + FastAPI + PostgreSQL + React + TypeScript**, executado com **Docker Compose**.

O projeto possui autenticação com JWT, cadastro de usuários, clientes, serviços, profissionais, horários de funcionamento, bloqueios, agendamentos, dashboard e relatórios.

![Runtime Verification](https://github.com/Edudsprado/Sistema-agendamento/actions/workflows/runtime-verification.yml/badge.svg)

---

## ✅ Estado atual do projeto

O sistema foi atualizado com melhorias de segurança e validação:

- `SECRET_KEY` obrigatória, sem fallback inseguro.
- Senha de login limitada a 128 caracteres.
- JWT com `jti` para identificação do token.
- Logout com revogação de token.
- Rate limiting básico para tentativas de login.
- E-mail normalizado no cadastro e no login.
- Docker Compose exigindo variáveis sensíveis via `.env`.
- Backend e frontend executando com usuário não-root nos containers.
- Frontend servido pelo Nginx na porta interna `8080`.
- Workflow de verificação no GitHub Actions com testes automatizados e smoke tests com Docker Compose.

> Observação: a revogação de token e o rate limiting atuais usam memória do processo. Para produção com múltiplas réplicas, o recomendado é migrar esses controles para Redis ou outro armazenamento compartilhado.

---

## 🚀 Início rápido

### Requisitos

Antes de começar, instale:

- Docker Desktop
- Git

No Windows, deixe o **Docker Desktop aberto e em execução** antes de subir o projeto.

---

## 1. Baixar o projeto

```bash
git clone https://github.com/Edudsprado/Sistema-agendamento.git
cd Sistema-agendamento
```

Confira a estrutura:

```text
backend
frontend
docker-compose.yml
README.md
.env.example
```

---

## 2. Configurar o ambiente

O projeto agora exige variáveis de ambiente sensíveis. Crie o arquivo `.env` a partir do exemplo.

### PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux, macOS ou Git Bash

```bash
cp .env.example .env
```

Depois edite o arquivo `.env`.

### Exemplo de `.env` local

```env
POSTGRES_DB=agendapro
POSTGRES_USER=agendapro
POSTGRES_PASSWORD=troque-esta-senha-local
DATABASE_URL=postgresql+psycopg://agendapro:troque-esta-senha-local@db:5432/agendapro
SECRET_KEY=gere-uma-chave-forte-e-unica
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
VITE_API_URL=http://localhost:8000
```

Gere uma `SECRET_KEY` forte com:

```bash
openssl rand -hex 32
```

No Windows, caso não tenha `openssl`, use uma senha longa, aleatória e exclusiva para desenvolvimento local.

> ⚠️ Nunca envie o arquivo `.env` para o GitHub.

---

## 3. Iniciar o sistema

Na pasta raiz do projeto, execute:

```bash
docker compose up --build
```

O Docker irá:

1. Criar o PostgreSQL.
2. Criar o backend FastAPI.
3. Criar o frontend React/Nginx.
4. Executar as migrations do banco.
5. Iniciar os serviços.

Na primeira execução, o processo pode demorar porque as imagens e dependências serão construídas.

---

## 4. Acessar o sistema

Depois que os containers estiverem em execução:

### Sistema

```text
http://localhost:3000
```

### API

```text
http://localhost:8000
```

### Documentação da API

```text
http://localhost:8000/docs
```

### Healthcheck

```text
http://localhost:8000/api/health
```

---

## 5. Primeiro acesso

Na tela inicial, clique em **Cadastre-se**.

Crie um usuário com:

- Nome.
- E-mail válido.
- Senha com pelo menos 8 caracteres.

Depois faça login normalmente.

---

## 6. Ordem recomendada de uso

Depois de entrar, configure o sistema nesta ordem:

```text
1. Clientes
2. Serviços
3. Profissionais
4. Horários de funcionamento
5. Bloqueios
6. Agendamentos
```

Exemplo de serviço:

```text
Nome: Corte
Duração: 30 minutos
Preço: R$ 45,00
```

Depois crie um profissional, associe o serviço, configure os horários e realize o primeiro agendamento.

---

## 7. Regras de conflito de horários

O backend valida automaticamente:

- Cliente ativo.
- Profissional ativo.
- Serviço ativo.
- Associação entre profissional e serviço.
- Horário de funcionamento.
- Bloqueios de horário.
- Duração do serviço.
- Conflitos com outros agendamentos.

Exemplo:

```text
Agendamento 1
14:00 → 14:30
```

Um segundo agendamento para o mesmo profissional:

```text
14:15 → 14:45
```

será recusado.

A validação acontece no **backend**, não apenas no frontend.

---

## 8. Autenticação e segurança

O projeto utiliza:

- JWT assinado com `SECRET_KEY`.
- Campo `jti` no token.
- Revogação de token no logout.
- Hash de senha com Argon2 via `pwdlib`.
- Validação de dados com Pydantic.
- Rotas protegidas por Bearer Token.
- Rate limiting básico no endpoint de login.
- CORS configurável por variável de ambiente.

Endpoints de autenticação:

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

Comportamentos esperados:

- Login válido retorna `access_token`.
- Senha incorreta retorna erro genérico.
- Token inválido retorna `401`.
- Token revogado após logout não pode ser reutilizado.
- Muitas tentativas de login retornam `429`.
- Senha acima de 128 caracteres no login retorna erro de validação.

---

## 9. Parar o sistema

Para parar os containers sem apagar os dados:

```bash
docker compose down
```

Para parar e apagar o volume do banco:

```bash
docker compose down -v
```

> ⚠️ `docker compose down -v` apaga os dados armazenados no PostgreSQL.

---

## 10. Atualizar o projeto

Quando houver novas alterações no GitHub:

```bash
git pull
docker compose up --build
```

---

## 11. Verificar containers e logs

Ver containers:

```bash
docker compose ps
```

Ver logs gerais:

```bash
docker compose logs -f
```

Ver logs por serviço:

```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

Reiniciar um serviço:

```bash
docker compose restart backend
docker compose restart frontend
docker compose restart db
```

---

## 🐍 Backend

Tecnologias:

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- Pydantic 2
- Alembic
- PostgreSQL
- PyJWT
- Argon2 / pwdlib
- Pytest

Principais recursos:

- Autenticação.
- Clientes.
- Serviços.
- Profissionais.
- Horários.
- Bloqueios.
- Agendamentos.
- Dashboard.
- Relatórios.
- Controle de conflitos.

---

## ⚛️ Frontend

Tecnologias:

- React
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query
- Lucide Icons
- Sonner
- Nginx para servir o build em Docker

A aplicação fica disponível em:

```text
http://localhost:3000
```

Internamente, o Nginx escuta na porta `8080` dentro do container.

---

## 🗄️ Banco de dados

O PostgreSQL roda em container Docker.

As credenciais devem ser configuradas no `.env`:

```env
POSTGRES_DB=agendapro
POSTGRES_USER=agendapro
POSTGRES_PASSWORD=sua-senha-local
DATABASE_URL=postgresql+psycopg://agendapro:sua-senha-local@db:5432/agendapro
```

Os dados são armazenados no volume:

```text
postgres_data
```

Esse volume mantém os dados mesmo após parar os containers com `docker compose down`.

---

## 📁 Estrutura do projeto

```text
Sistema-agendamento/
│
├── .github/
│   └── workflows/
│       └── runtime-verification.yml
│
├── backend/
│   ├── app/
│   │   ├── appointment_service.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testes

### Testes do backend

```bash
cd backend
PYTHONPATH=. pytest -q
```

No PowerShell:

```powershell
cd backend
$env:PYTHONPATH="."
pytest -q
```

### Testar build do frontend

```bash
cd frontend
npm install
npm run build
```

### Verificação automatizada no GitHub Actions

O repositório possui a workflow:

```text
.github/workflows/runtime-verification.yml
```

Ela executa:

- Instalação das dependências do backend.
- Testes com `pytest`.
- Build e subida da aplicação com Docker Compose.
- Verificação do `/api/health`.
- Verificação do frontend em `localhost:3000`.
- Smoke tests reais de autenticação via HTTP.

Smoke tests cobertos:

- Cadastro de usuário.
- Consulta de `/api/auth/me` com token válido.
- Acesso ao dashboard autenticado.
- Bloqueio de dashboard sem token.
- Rejeição de token inválido.
- Rejeição de senha longa no login.
- Rate limiting após tentativas inválidas.
- Logout.
- Rejeição de token revogado após logout.

---

## 🔌 Principais endpoints

### Autenticação

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

### Clientes

```text
GET    /api/clients
POST   /api/clients
GET    /api/clients/{id}
PUT    /api/clients/{id}
DELETE /api/clients/{id}
```

### Serviços

```text
GET    /api/services
POST   /api/services
GET    /api/services/{id}
PUT    /api/services/{id}
DELETE /api/services/{id}
```

### Profissionais

```text
GET    /api/professionals
POST   /api/professionals
GET    /api/professionals/{id}
PUT    /api/professionals/{id}
DELETE /api/professionals/{id}
```

### Horários de funcionamento

```text
GET /api/business-hours
PUT /api/business-hours
```

### Bloqueios

```text
GET    /api/blocked-times
POST   /api/blocked-times
PUT    /api/blocked-times/{id}
DELETE /api/blocked-times/{id}
```

### Agendamentos

```text
GET    /api/appointments
POST   /api/appointments
GET    /api/appointments/{id}
PUT    /api/appointments/{id}
DELETE /api/appointments/{id}
PATCH  /api/appointments/{id}/status
```

### Dashboard

```text
GET /api/dashboard
```

### Relatórios

```text
GET /api/reports/appointments
GET /api/reports/revenue
GET /api/reports/services
GET /api/reports/cancellations
```

---

## 🆘 Solução de problemas

### Erro: `POSTGRES_PASSWORD obrigatória`, `DATABASE_URL obrigatória` ou `SECRET_KEY obrigatória`

Crie e configure o arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Depois preencha as variáveis obrigatórias.

---

### Erro: `no configuration file provided`

Você provavelmente está fora da pasta raiz do projeto.

```bash
cd Sistema-agendamento
docker compose up --build
```

---

### Erro relacionado ao Docker Desktop

Confirme se o Docker Desktop está aberto e pronto:

```bash
docker info
```

Depois execute novamente:

```bash
docker compose up --build
```

---

### Erro de porta ocupada

O projeto utiliza:

```text
Frontend externo → 3000
Backend externo  → 8000
PostgreSQL interno → 5432
```

Se alguma porta estiver ocupada, pare o outro serviço ou ajuste o mapeamento no `docker-compose.yml`.

---

### Alterei o `.env` e nada mudou

Recrie os containers:

```bash
docker compose down
docker compose up --build
```

---

## 🚀 Fluxo rápido para nova máquina

```bash
git clone https://github.com/Edudsprado/Sistema-agendamento.git
cd Sistema-agendamento
cp .env.example .env
# edite o .env antes de continuar
docker compose up --build
```

Depois abra:

```text
http://localhost:3000
```

---

## 👨‍💻 Desenvolvimento

Fluxo comum:

```bash
git pull
# edite os arquivos
git add .
git commit -m "descricao da alteracao"
git push
```

Atualizar o ambiente Docker:

```bash
docker compose up --build
```

Executar testes antes de enviar alterações:

```bash
cd backend
PYTHONPATH=. pytest -q
```

---

## 📌 Projeto

**AgendaPro**

Sistema de gerenciamento de agendamentos com:

```text
Python
FastAPI
PostgreSQL
React
TypeScript
Docker
```

Repositório:

```text
https://github.com/Edudsprado/Sistema-agendamento
```
