# Sistema de Agendamento

Sistema de autoagendamento online para clínicas e empresas de serviços. O cliente agenda diretamente pelo site — confirmação automática, sem aprovação manual.

## Contexto

Desenvolvido como projeto acadêmico com aplicação prática em agências de landing page e sites institucionais (nichos de saúde, estética e afins).

## Fluxo principal

1. Cliente acessa o site e escolhe serviço, profissional, data e horário
2. Preenche nome, telefone e e-mail
3. Slot é bloqueado atomicamente no banco
4. Notificação automática via WhatsApp ou e-mail
5. Cliente pode cancelar ou reagendar pelo link da notificação
6. Recepcionista gerencia tudo pelo painel admin

## Stack

- **Backend:** Python + FastAPI
- **Banco de dados:** PostgreSQL
- **ORM:** SQLAlchemy + Alembic (migrations)
- **Notificações:** WhatsApp (Twilio/Z-API) + e-mail (SendGrid/SMTP)
- **Frontend:** A definir (React ou Lovable)

## Status

- [x] Fluxo de usuário definido
- [x] Schema do banco de dados modelado
- [ ] Backend (FastAPI)
- [ ] Notificações
- [ ] Frontend cliente
- [ ] Painel admin
