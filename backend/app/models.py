import enum
from datetime import date, datetime, time, timezone
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Index, Integer, Numeric, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def now(): return datetime.now(timezone.utc)
class AppointmentStatus(str, enum.Enum):
    scheduled="scheduled"; confirmed="confirmed"; completed="completed"; cancelled="cancelled"; no_show="no_show"
class Owned:
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(100)); email: Mapped[str]=mapped_column(String(255),unique=True,index=True); password_hash: Mapped[str]=mapped_column(String(255)); active: Mapped[bool]=mapped_column(Boolean,default=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
class Client(Owned,Base):
    __tablename__="clients"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(120),index=True); phone: Mapped[str|None]=mapped_column(String(30)); email: Mapped[str|None]=mapped_column(String(255)); notes: Mapped[str|None]=mapped_column(Text); active: Mapped[bool]=mapped_column(Boolean,default=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
class Service(Owned,Base):
    __tablename__="services"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(120),index=True); description: Mapped[str|None]=mapped_column(Text); duration_minutes: Mapped[int]=mapped_column(Integer); price: Mapped[Decimal]=mapped_column(Numeric(10,2)); active: Mapped[bool]=mapped_column(Boolean,default=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
class ProfessionalService(Base):
    __tablename__="professional_services"; __table_args__=(UniqueConstraint("professional_id","service_id"),)
    id: Mapped[int]=mapped_column(primary_key=True); professional_id: Mapped[int]=mapped_column(ForeignKey("professionals.id",ondelete="CASCADE")); service_id: Mapped[int]=mapped_column(ForeignKey("services.id",ondelete="CASCADE"))
class Professional(Owned,Base):
    __tablename__="professionals"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(120),index=True); phone: Mapped[str|None]=mapped_column(String(30)); email: Mapped[str|None]=mapped_column(String(255)); notes: Mapped[str|None]=mapped_column(Text); active: Mapped[bool]=mapped_column(Boolean,default=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
    services: Mapped[list[Service]]=relationship(secondary="professional_services",lazy="selectin")
class BusinessHour(Owned,Base):
    __tablename__="business_hours"; __table_args__=(UniqueConstraint("owner_id","weekday"),)
    id: Mapped[int]=mapped_column(primary_key=True); weekday: Mapped[int]=mapped_column(Integer); start_time: Mapped[time]=mapped_column(Time); end_time: Mapped[time]=mapped_column(Time); active: Mapped[bool]=mapped_column(Boolean,default=True)
class BlockedTime(Owned,Base):
    __tablename__="blocked_times"
    id: Mapped[int]=mapped_column(primary_key=True); professional_id: Mapped[int|None]=mapped_column(ForeignKey("professionals.id",ondelete="CASCADE"),nullable=True); date: Mapped[date]=mapped_column(Date,index=True); start_time: Mapped[time]=mapped_column(Time); end_time: Mapped[time]=mapped_column(Time); reason: Mapped[str]=mapped_column(String(180))
class Appointment(Owned,Base):
    __tablename__="appointments"; __table_args__=(Index("ix_appointments_professional_date","professional_id","date"),)
    id: Mapped[int]=mapped_column(primary_key=True); client_id: Mapped[int]=mapped_column(ForeignKey("clients.id")); service_id: Mapped[int]=mapped_column(ForeignKey("services.id")); professional_id: Mapped[int]=mapped_column(ForeignKey("professionals.id")); date: Mapped[date]=mapped_column(Date,index=True); start_time: Mapped[time]=mapped_column(Time); end_time: Mapped[time]=mapped_column(Time); status: Mapped[AppointmentStatus]=mapped_column(Enum(AppointmentStatus),default=AppointmentStatus.scheduled,index=True); price: Mapped[Decimal]=mapped_column(Numeric(10,2)); notes: Mapped[str|None]=mapped_column(Text); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)
    client: Mapped[Client]=relationship(lazy="joined"); service: Mapped[Service]=relationship(lazy="joined"); professional: Mapped[Professional]=relationship(lazy="joined")
