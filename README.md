# AgendaPro

Sistema full-stack de agendamentos para clínicas, salões, barbearias, oficinas e prestadores de serviços. Inclui autenticação JWT, CRUDs, agenda, bloqueio real de conflitos, calendário, painel e relatórios.

## Tecnologias
- **API:** Python 3.12, FastAPI, SQLAlchemy 2, Pydantic 2, Alembic, PostgreSQL, PyJWT e Argon2.
- **Interface:** React 19, TypeScript, Vite, Tailwind CSS e TanStack Query.
- **Ambiente:** Docker Compose, com serviços isolados para banco, API e interface.

## Início rápido com Docker
1. Copie `.env.example` para `.env` e substitua `SECRET_KEY` por uma chave forte.
2. Execute `docker compose up --build`.
3. Acesse a interface em http://localhost:3000 e a documentação da API em http://localhost:8000/docs.
4. As migrations são aplicadas automaticamente ao iniciar a API.

Os dados do PostgreSQL persistem no volume `postgres_data`. Para apagar tudo: `docker compose down -v`.

## Execução manual
### Banco e API
Tenha Python 3.12+ e PostgreSQL disponíveis. Crie o banco `agendapro`, copie `.env.example` para `backend/.env` e ajuste `DATABASE_URL`.

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Interface
Tenha Node.js 20+ instalado.
```bash
cd frontend
npm install
# opcional: defina VITE_API_URL=http://localhost:8000 em .env
npm run dev
```
Acesse http://localhost:5173.

## Organização
- `backend/app/main.py`: endpoints REST, autenticação, painel e relatórios.
- `backend/app/models.py`: modelos e relacionamentos do PostgreSQL.
- `backend/app/appointment_service.py`: regra transacional de disponibilidade.
- `backend/alembic`: migrations.
- `backend/tests`: testes automatizados.
- `frontend/src`: interface, estado e comunicação com a API.

## Segurança e autenticação
As senhas usam hash Argon2 e nunca são devolvidas pela API. Após cadastro ou login, a API retorna JWT Bearer. Todas as operações de negócio exigem esse token e são isoladas por proprietário. Configure CORS e o segredo por ambiente. Em produção, use HTTPS, uma `SECRET_KEY` longa e restrinja `CORS_ORIGINS` ao domínio real.

O logout remove o token no cliente. JWTs já emitidos expiram conforme `ACCESS_TOKEN_EXPIRE_MINUTES`; para revogação imediata, adicione uma lista de revogação persistente.

## Endpoints
- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/logout`
- CRUD: `/api/clients`, `/api/services`, `/api/professionals`, `/api/blocked-times`, `/api/appointments`
- `GET/PUT /api/business-hours`
- `PATCH /api/appointments/{id}/status`
- `GET /api/dashboard`
- `GET /api/reports/appointments`, `/revenue`, `/services`, `/cancellations`

Filtros de agendamentos: `start`, `end`, `professional_id`, `service_id`, `client_id` e `status`. A documentação interativa completa está em `/docs`.

## Regra de disponibilidade
Antes de criar ou editar, a API valida cliente, serviço e profissional ativos, associação profissional-serviço, expediente do dia, bloqueios gerais ou individuais e sobreposição. O horário final é calculado pela duração do serviço. Agendamentos cancelados liberam o período.

## Dados de demonstração (opcional)
Após as migrations, rode `python -m app.seed`. Isso cria `admin@agendapro.local`, senha `Agenda123!`, e exemplos. Nunca use essa senha em produção. Os dados podem ser removidos pela interface ou recriando o volume. O seed não roda automaticamente.

## Testes
Os testes usam um banco SQLite isolado e cobrem cadastro, login, CRUD essencial, associação de serviço, cálculo do término, conflito, expediente, bloqueio, status, relatórios e exclusão.
```bash
cd backend
pytest -q
```
Para validar a interface: `cd frontend && npm run build`.

## Roteiro funcional
Cadastre a conta, entre, crie cliente e serviço, crie profissional escolhendo o serviço, ajuste o expediente, crie um bloqueio e depois um agendamento em horário livre. Tente outro no mesmo intervalo para conferir a rejeição. Use as ações da lista para confirmar, concluir ou cancelar e confira os totais no painel e relatórios.

## Deploy
Publique o frontend como arquivos estáticos e a API em um serviço compatível com contêiner Python. Use PostgreSQL gerenciado, execute `alembic upgrade head` na implantação, defina todas as variáveis de ambiente e altere `VITE_API_URL` para a URL HTTPS pública da API. Não publique `.env`.
