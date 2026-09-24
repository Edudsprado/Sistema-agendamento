from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app import models, schemas

def validate_and_build(db:Session,owner_id:int,data:schemas.AppointmentIn,exclude_id:int|None=None):
    client=db.scalar(select(models.Client).where(models.Client.id==data.client_id,models.Client.owner_id==owner_id,models.Client.active))
    service=db.scalar(select(models.Service).where(models.Service.id==data.service_id,models.Service.owner_id==owner_id,models.Service.active))
    professional=db.scalar(select(models.Professional).where(models.Professional.id==data.professional_id,models.Professional.owner_id==owner_id,models.Professional.active))
    if not client: raise HTTPException(400,"Cliente inválido ou inativo")
    if not service: raise HTTPException(400,"Serviço inválido ou inativo")
    if not professional: raise HTTPException(400,"Profissional inválido ou inativo")
    linked=db.scalar(select(models.ProfessionalService).where(models.ProfessionalService.professional_id==professional.id,models.ProfessionalService.service_id==service.id))
    if not linked: raise HTTPException(400,"O profissional não realiza este serviço")
    start=datetime.combine(data.date,data.start_time); end=start+timedelta(minutes=service.duration_minutes)
    hours=db.scalar(select(models.BusinessHour).where(models.BusinessHour.owner_id==owner_id,models.BusinessHour.weekday==data.date.weekday(),models.BusinessHour.active))
    if not hours or data.start_time<hours.start_time or end.time()>hours.end_time: raise HTTPException(409,"Horário fora do expediente")
    blocked=db.scalar(select(models.BlockedTime).where(models.BlockedTime.owner_id==owner_id,models.BlockedTime.date==data.date,or_(models.BlockedTime.professional_id.is_(None),models.BlockedTime.professional_id==professional.id),models.BlockedTime.start_time<end.time(),models.BlockedTime.end_time>data.start_time))
    if blocked: raise HTTPException(409,"Horário bloqueado")
    q=select(models.Appointment).where(models.Appointment.owner_id==owner_id,models.Appointment.professional_id==professional.id,models.Appointment.date==data.date,models.Appointment.status.notin_([models.AppointmentStatus.cancelled]),models.Appointment.start_time<end.time(),models.Appointment.end_time>data.start_time).with_for_update()
    if exclude_id: q=q.where(models.Appointment.id!=exclude_id)
    if db.scalar(q): raise HTTPException(409,"Já existe um agendamento nesse horário")
    return {**data.model_dump(exclude={"price"}),"end_time":end.time(),"price":data.price if data.price is not None else service.price,"owner_id":owner_id}
