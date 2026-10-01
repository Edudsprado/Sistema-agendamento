# 📅 AgendaPro

Sistema de agendamento desenvolvido com **Python + FastAPI + PostgreSQL + React + TypeScript**, executado com **Docker Compose**.

![Runtime Verification](https://github.com/Edudsprado/Sistema-agendamento/actions/workflows/runtime-verification.yml/badge.svg)

---

## 🎓 Disciplina

**Universidade de Cuiabá — UNIC**  
**Curso:** Ciência da Computação  
**Disciplina:** Desenvolvimento de Soluções Remotas  
**Professor:** Felipe Douglas

---

## 📌 Finalidade do projeto

Este projeto tem finalidade **acadêmica**, desenvolvido como atividade da disciplina **Desenvolvimento de Soluções Remotas**.

O objetivo é demonstrar a criação de uma aplicação web completa, com frontend, backend, banco de dados, autenticação, conteinerização e testes automatizados.

Além da entrega acadêmica, o projeto também serve como uma **base inicial para futuros projetos de implantação de sistemas**, podendo ser evoluído para cenários mais completos de produção, integração, segurança, monitoramento e deploy.

---

## ✅ Funcionalidades principais

- Cadastro e login de usuários.
- Autenticação com JWT.
- Logout com revogação de token.
- Rate limiting básico no login.
- Cadastro de clientes.
- Cadastro de serviços.
- Cadastro de profissionais.
- Configuração de horários de funcionamento.
- Bloqueio de horários.
- Controle de agendamentos.
- Dashboard e relatórios.
- Validação de conflitos de horário no backend.

---

## 🧰 Tecnologias utilizadas

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- PyJWT
- Argon2 / pwdlib
- Pytest

### Frontend

- React
- TypeScript
- Vite
- TanStack Query
- Tailwind CSS
- Nginx

### Infraestrutura

- Docker
- Docker Compose
- GitHub Actions

---

## 📁 Estrutura do projeto

```text
Sistema-agendamento/
├── .github/workflows/
│   └── runtime-verification.yml
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Sobre o arquivo `.env`

O projeto usa variáveis de ambiente para separar configurações sensíveis do código.

O arquivo `.env.example` fica no GitHub apenas como modelo. Já o arquivo `.env` real deve ser criado localmente e **não deve ser enviado para o repositório**, pois contém senha do banco, chave JWT e outras configurações do ambiente.

Crie o `.env` a partir do modelo:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux, macOS ou Git Bash

```bash
cp .env.example .env
```

Depois edite o arquivo `.env` com seus valores locais:

```env
POSTGRES_DB=agendapro
POSTGRES_USER=agendapro
POSTGRES_PASSWORD=troque-por-uma-senha-forte
DATABASE_URL=postgresql+psycopg://agendapro:troque-por-uma-senha-forte@db:5432/agendapro
SECRET_KEY=gere-uma-chave-forte-e-unica
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
VITE_API_URL=http://localhost:8000
```

Para gerar uma chave forte em ambientes com OpenSSL:

```bash
openssl rand -hex 32
```

---

## 🚀 Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/Edudsprado/Sistema-agendamento.git
cd Sistema-agendamento
```

Crie e configure o `.env`:

```bash
cp .env.example .env
```

Suba os containers:

```bash
docker compose up --build
```

Acesse:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs
Health:   http://localhost:8000/api/health
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

### Teste de build do frontend

```bash
cd frontend
npm install
npm run build
```

### Verificação automatizada

O projeto possui uma workflow no GitHub Actions:

```text
.github/workflows/runtime-verification.yml
```

Ela executa:

- testes do backend;
- build e subida da aplicação com Docker Compose;
- verificação do backend;
- verificação do frontend;
- testes reais de autenticação via HTTP.

---

## 🔌 Principais endpoints

### Autenticação

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

### Recursos principais

```text
GET/POST/PUT/DELETE /api/clients
GET/POST/PUT/DELETE /api/services
GET/POST/PUT/DELETE /api/professionals
GET/PUT             /api/business-hours
GET/POST/PUT/DELETE /api/blocked-times
GET/POST/PUT/DELETE /api/appointments
PATCH               /api/appointments/{id}/status
GET                 /api/dashboard
GET                 /api/reports/appointments
GET                 /api/reports/revenue
GET                 /api/reports/services
GET                 /api/reports/cancellations
```

---

## 🔒 Segurança aplicada

O projeto possui algumas medidas básicas de segurança para autenticação:

- senhas armazenadas com hash Argon2;
- JWT assinado por `SECRET_KEY`;
- token com identificador `jti`;
- logout com revogação de token;
- senha de login limitada a 128 caracteres;
- mensagens genéricas para erro de login;
- rate limiting básico contra tentativas repetidas;
- CORS configurável;
- variáveis sensíveis fora do código.

> Observação: a revogação de token e o rate limiting usam memória do processo. Para ambiente de produção com múltiplos containers, o ideal é migrar esses controles para Redis ou outro armazenamento compartilhado.

---

## 🛠️ Comandos úteis

Parar containers sem apagar dados:

```bash
docker compose down
```

Parar containers e apagar volume do banco:

```bash
docker compose down -v
```

Ver containers:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Reconstruir após alterações:

```bash
docker compose up --build
```

---

## 🆘 Problemas comuns

### Erro informando variável obrigatória

Se aparecer erro sobre `POSTGRES_PASSWORD`, `DATABASE_URL` ou `SECRET_KEY`, verifique se o arquivo `.env` existe na raiz do projeto e se as variáveis foram preenchidas.

### Porta ocupada

O projeto usa:

```text
Frontend: 3000
Backend: 8000
```

Se alguma porta estiver ocupada, encerre o serviço que está usando a porta ou altere o mapeamento no `docker-compose.yml`.

### Alterei o `.env` e nada mudou

Recrie os containers:

```bash
docker compose down
docker compose up --build
```

---

## 📚 Observação final

Este sistema foi desenvolvido com fins acadêmicos e pode ser utilizado como ponto de partida para estudos e futuras evoluções, incluindo deploy, monitoramento, autenticação avançada, integração com serviços externos e implantação em ambientes reais.
