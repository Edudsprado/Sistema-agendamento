import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey,
    Integer, Numeric, String, Time, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class StatusAgendamento(str, PyEnum):
    confirmado = "confirmado"
    cancelado = "cancelado"
    reagendado = "reagendado"


class CanalNotificacao(str, PyEnum):
    whatsapp = "whatsapp"
    email = "email"


class StatusNotificacao(str, PyEnum):
    pendente = "pendente"
    enviado = "enviado"
    falhou = "falhou"


class TipoNotificacao(str, PyEnum):
    confirmacao = "confirmacao"
    cancelamento = "cancelamento"
    reagendamento = "reagendamento"
    lembrete = "lembrete"


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    agendamentos = relationship("Agendamento", back_populates="cliente")


class Servico(Base):
    __tablename__ = "servico"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    duracao_min = Column(Integer, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    agendamentos = relationship("Agendamento", back_populates="servico")


class Profissional(Base):
    __tablename__ = "profissional"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    ativo = Column(Boolean, default=True, nullable=False)

    agendamentos = relationship("Agendamento", back_populates="profissional")
    disponibilidades = relationship("Disponibilidade", back_populates="profissional")


class Disponibilidade(Base):
    __tablename__ = "disponibilidade"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profissional_id = Column(UUID(as_uuid=True), ForeignKey("profissional.id"), nullable=False)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    profissional = relationship("Profissional", back_populates="disponibilidades")


class Agendamento(Base):
    __tablename__ = "agendamento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("cliente.id"), nullable=False)
    servico_id = Column(UUID(as_uuid=True), ForeignKey("servico.id"), nullable=False)
    profissional_id = Column(UUID(as_uuid=True), ForeignKey("profissional.id"), nullable=False)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.confirmado, nullable=False)
    notificacao_canal = Column(Enum(CanalNotificacao), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("profissional_id", "data_hora_inicio", name="uq_profissional_slot"),
    )

    cliente = relationship("Cliente", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    profissional = relationship("Profissional", back_populates="agendamentos")
    notificacoes = relationship("Notificacao", back_populates="agendamento")


class Notificacao(Base):
    __tablename__ = "notificacao"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agendamento_id = Column(UUID(as_uuid=True), ForeignKey("agendamento.id"), nullable=False)
    tipo = Column(Enum(TipoNotificacao), nullable=False)
    canal = Column(Enum(CanalNotificacao), nullable=False)
    status = Column(Enum(StatusNotificacao), default=StatusNotificacao.pendente, nullable=False)
    enviado_em = Column(DateTime, nullable=True)

    agendamento = relationship("Agendamento", back_populates="notificacoes")
