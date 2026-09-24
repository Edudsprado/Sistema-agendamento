# 📅 AgendaPro

Sistema completo de agendamento, desenvolvido com **Python + FastAPI + PostgreSQL + React + TypeScript**, executado facilmente com **Docker Compose**.

O projeto foi organizado para que uma nova instalação possa ser feita com poucos comandos.

---

## 🚀 Início rápido

### Requisitos

Antes de começar, instale:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Git

No Windows, deixe o **Docker Desktop aberto e em execução**.

---

# 1. Baixar o projeto

Abra o PowerShell ou Git Bash e execute:

```bash
git clone https://github.com/Edudsprado/Sistema-agendamento.git
```

Entre na pasta:

```bash
cd Sistema-agendamento
```

Confira se os arquivos estão presentes:

```bash
dir
```

Você deverá encontrar:

```text
backend
frontend
docker-compose.yml
README.md
.env.example
```

---

# 2. Configuração do ambiente

Para uso local com Docker, o projeto já possui configurações padrão.

Opcionalmente, crie o arquivo `.env` a partir do modelo:

### PowerShell

```powershell
Copy-Item .env.example .env
```

Depois, abra:

```powershell
notepad .env
```

Exemplo:

```env
SECRET_KEY=troque-por-uma-chave-secreta
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

> ⚠️ O arquivo `.env` não deve ser enviado para o GitHub.

Para uso local, o Docker Compose já configura automaticamente a comunicação entre PostgreSQL, backend e frontend.

---

# 3. Iniciar o sistema

Na pasta:

```text
Sistema-agendamento
```

execute:

```bash
docker compose up --build
```

O Docker irá:

1. Criar o PostgreSQL
2. Criar o backend Python/FastAPI
3. Criar o frontend React
4. Executar as migrations do banco
5. Iniciar os serviços

Na primeira execução pode demorar um pouco porque as imagens e dependências serão construídas.

---

# 4. Acessar o sistema

Depois que os containers estiverem iniciados:

### 🖥️ Sistema

```text
http://localhost:3000
```

### 🔧 API

```text
http://localhost:8000
```

### 📚 Documentação da API

```text
http://localhost:8000/docs
```

A documentação `/docs` permite testar os endpoints da API diretamente pelo navegador.

---

# 5. Primeiro acesso

Na tela inicial, clique em:

```text
Cadastre-se
```

Crie seu usuário com:

* Nome
* E-mail válido
* Senha com pelo menos 8 caracteres

Depois faça login.

> Use um e-mail real ou um domínio aceito pelo validador. Evite endereços como `usuario@agendapro.local`.

---

# 6. Ordem recomendada para configurar o sistema

Depois de entrar, configure nesta ordem:

```text
1. Clientes
2. Serviços
3. Profissionais
4. Horários de funcionamento
5. Bloqueios
6. Agendamentos
```

### Exemplo

Crie um serviço:

```text
Nome: Corte
Duração: 30 minutos
Preço: R$ 45,00
```

Depois crie um profissional e associe o serviço.

Configure o horário de funcionamento e então faça o primeiro agendamento.

---

# 7. Regra de conflito de horários

O backend verifica automaticamente:

* profissional ativo;
* serviço ativo;
* associação entre profissional e serviço;
* horário de funcionamento;
* bloqueios;
* duração do serviço;
* conflitos com outros agendamentos.

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

A validação acontece no **backend Python**, e não somente no frontend.

---

# 8. Parar o sistema

Para parar os containers:

```bash
docker compose down
```

Isso **não apaga os dados do banco**.

---

# 9. Iniciar novamente

Depois que o projeto já tiver sido construído, normalmente basta:

```bash
docker compose up
```

---

# 10. Reconstruir o projeto

Sempre que houver alteração no código e você quiser garantir que as imagens sejam reconstruídas:

```bash
docker compose up --build
```

---

# 11. Atualizar o projeto pelo GitHub

Caso exista uma versão nova no GitHub:

```bash
git pull
```

Depois:

```bash
docker compose up --build
```

Assim você baixa as alterações e reconstrói os containers.

---

# 12. Verificar os containers

Para verificar se todos os serviços estão funcionando:

```bash
docker compose ps
```

O projeto possui os seguintes serviços:

```text
db
backend
frontend
```

---

# 13. Ver logs

Para visualizar os logs:

```bash
docker compose logs -f
```

Para visualizar somente o backend:

```bash
docker compose logs -f backend
```

Para visualizar somente o frontend:

```bash
docker compose logs -f frontend
```

Para visualizar somente o banco:

```bash
docker compose logs -f db
```

Para sair dos logs:

```text
Ctrl + C
```

---

# 14. Reiniciar apenas um serviço

Backend:

```bash
docker compose restart backend
```

Frontend:

```bash
docker compose restart frontend
```

Banco:

```bash
docker compose restart db
```

---

# 15. Resetar completamente o banco

⚠️ **ATENÇÃO: isso apaga os dados cadastrados no PostgreSQL.**

```bash
docker compose down -v
```

Depois recrie tudo:

```bash
docker compose up --build
```

Use essa opção somente quando realmente quiser começar com o banco vazio.

---

# 🐍 Backend

O backend foi desenvolvido em:

* Python 3.12+
* FastAPI
* SQLAlchemy 2
* Pydantic 2
* Alembic
* PostgreSQL
* JWT
* Argon2

Principais recursos:

* autenticação;
* clientes;
* serviços;
* profissionais;
* horários;
* bloqueios;
* agendamentos;
* dashboard;
* relatórios;
* controle de conflitos.

---

# ⚛️ Frontend

O frontend utiliza:

* React
* TypeScript
* Vite
* Tailwind CSS
* TanStack Query
* Lucide Icons
* Sonner

Interface responsiva para:

* computador;
* tablet;
* celular.

---

# 🗄️ Banco de dados

O PostgreSQL é executado em container Docker.

Banco:

```text
agendapro
```

Usuário:

```text
agendapro
```

Senha local:

```text
agendapro
```

Os dados são armazenados no volume:

```text
postgres_data
```

Isso permite que os dados permaneçam mesmo depois de parar os containers.

---

# 📁 Estrutura do projeto

```text
Sistema-agendamento/
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

# 🔐 Segurança

O projeto utiliza:

* JWT;
* hash de senha com Argon2;
* validação de dados;
* CORS;
* rotas protegidas;
* variáveis de ambiente.

Nunca publique:

```text
.env
```

no GitHub.

Para produção, utilize:

* HTTPS;
* `SECRET_KEY` forte e exclusiva;
* PostgreSQL gerenciado;
* CORS limitado ao domínio da aplicação.

---

# 🧪 Testes

Para executar os testes do backend manualmente:

```bash
cd backend
pytest -q
```

Para testar o build do frontend:

```bash
cd frontend
npm install
npm run build
```

---

# 🔌 Principais endpoints

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

# 🆘 Solução de problemas

## Erro: `no configuration file provided`

Você provavelmente está na pasta errada.

Entre na pasta do projeto:

```bash
cd Sistema-agendamento
```

Depois:

```bash
docker compose up --build
```

---

## Erro: `dockerDesktopLinuxEngine`

O Docker Desktop não está executando.

Abra o:

```text
Docker Desktop
```

aguarde o Docker ficar pronto e execute:

```bash
docker info
```

Depois:

```bash
docker compose up --build
```

---

## Erro de porta ocupada

O projeto utiliza:

```text
Frontend → 3000
Backend  → 8000
PostgreSQL → 5432
```

Verifique se outra aplicação está utilizando essas portas.

---

# 🚀 Fluxo rápido para uma nova máquina

Depois de instalar Docker Desktop e Git:

```bash
git clone https://github.com/Edudsprado/Sistema-agendamento.git
cd Sistema-agendamento
docker compose up --build
```

Depois abra:

```text
http://localhost:3000
```

É isso.

---

# 👨‍💻 Desenvolvimento

Para alterações no projeto:

```bash
git pull
```

Edite os arquivos.

Depois:

```bash
git add .
git commit -m "descricao da alteracao"
git push
```

Em seguida, para atualizar o ambiente Docker:

```bash
docker compose up --build
```

---

# 📌 Projeto

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

https://github.com/Edudsprado/Sistema-agendamento
