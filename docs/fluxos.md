# Fluxos do sistema

## Atores
- **Cliente:** agenda pelo site
- **Recepcionista:** gerencia pelo painel admin

## Fluxo 1 — Autoagendamento
1. Escolhe serviço, profissional, data e horário
2. Preenche nome, telefone e e-mail
3. Slot bloqueado atomicamente
4. Status: confirmado imediatamente
5. Notificação enviada com link de gerenciamento

## Fluxo 2 — Cancelamento pelo cliente
1. Clica no link da notificação
2. Status muda para cancelado
3. Slot liberado no banco

## Fluxo 3 — Reagendamento pelo cliente
1. Clica no link da notificação
2. Escolhe novo horário disponível
3. Slot antigo liberado, novo bloqueado
4. Nova notificação enviada

## Regras de negócio
- Índice único (profissional_id, data_hora_inicio) impede conflito de slots
- data_hora_fim = data_hora_inicio + servico.duracao_min
- Notificações com falha ficam como "falhou" e podem ser reenviadas
