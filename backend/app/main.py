from datetime import date, time, timedelta
from decimal import Decimal
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import Base, engine
from app import models, schemas
from app.appointment_service import validate_and_build
from app.dependencies import current_user, get_db
from app.security import create_token, hash_password, verify_password
app=FastAPI(title="AgendaPro API",version="1.0.0",docs_url="/docs")
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.post("/api/auth/register",response_model=schemas.Token,status_code=201)
def register(data:schemas.Register,db:Session=Depends(get_db)):
    if db.scalar(select(models.User).where(func.lower(models.User.email)==data.email.lower())): raise HTTPException(409,"E-mail já cadastrado")
    user=models.User(name=data.name,email=data.email.lower(),password_hash=hash_password(data.password)); db.add(user); db.flush()
    for day in range(7): db.add(models.BusinessHour(owner_id=user.id,weekday=day,start_time=time(8,0),end_time=time(18,0),active=day<5))
    db.commit(); db.refresh(user); return schemas.Token(access_token=create_token(user.id),user=user)
@app.post("/api/auth/login",response_model=schemas.Token)
def login(data:schemas.Login,db:Session=Depends(get_db)):
    user=db.scalar(select(models.User).where(func.lower(models.User.email)==data.email.lower()))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"E-mail ou senha inválidos")
    return schemas.Token(access_token=create_token(user.id),user=user)
@app.get("/api/auth/me",response_model=schemas.UserOut)
def me(user=Depends(current_user)): return user
@app.post("/api/auth/logout",status_code=204)
def logout(user=Depends(current_user)): return None

def owned(model,id,user,db):
    obj=db.scalar(select(model).where(model.id==id,model.owner_id==user.id))
    if not obj: raise HTTPException(404,"Registro não encontrado")
    return obj

def crud_routes(path,model,in_schema,out_schema):
    @app.get(path,response_model=list[out_schema])
    def list_items(q:str|None=None,active:bool|None=None,db:Session=Depends(get_db),user=Depends(current_user)):
        stmt=select(model).where(model.owner_id==user.id)
        if q and hasattr(model,"name"): stmt=stmt.where(model.name.ilike(f"%{q}%"))
        if active is not None and hasattr(model,"active"): stmt=stmt.where(model.active==active)
        return list(db.scalars(stmt.order_by(model.id.desc())))
    @app.get(path+"/{item_id}",response_model=out_schema)
    def get_item(item_id:int,db:Session=Depends(get_db),user=Depends(current_user)): return owned(model,item_id,user,db)
    @app.post(path,response_model=out_schema,status_code=201)
    def create_item(data:in_schema,db:Session=Depends(get_db),user=Depends(current_user)):
        values=data.model_dump(); service_ids=values.pop("service_ids",None); obj=model(**values,owner_id=user.id); db.add(obj); db.flush()
        if service_ids is not None:
            services=list(db.scalars(select(models.Service).where(models.Service.owner_id==user.id,models.Service.id.in_(service_ids))))
            if len(services)!=len(set(service_ids)): raise HTTPException(400,"Serviço inválido")
            obj.services=services
        db.commit(); db.refresh(obj); return obj
    @app.put(path+"/{item_id}",response_model=out_schema)
    def update_item(item_id:int,data:in_schema,db:Session=Depends(get_db),user=Depends(current_user)):
        obj=owned(model,item_id,user,db); values=data.model_dump(); service_ids=values.pop("service_ids",None)
        for k,v in values.items(): setattr(obj,k,v)
        if service_ids is not None: obj.services=list(db.scalars(select(models.Service).where(models.Service.owner_id==user.id,models.Service.id.in_(service_ids))))
        db.commit(); db.refresh(obj); return obj
    @app.delete(path+"/{item_id}",status_code=204)
    def delete_item(item_id:int,db:Session=Depends(get_db),user=Depends(current_user)): db.delete(owned(model,item_id,user,db)); db.commit()
crud_routes("/api/clients",models.Client,schemas.ClientIn,schemas.ClientOut)
crud_routes("/api/services",models.Service,schemas.ServiceIn,schemas.ServiceOut)
crud_routes("/api/professionals",models.Professional,schemas.ProfessionalIn,schemas.ProfessionalOut)
@app.get("/api/business-hours",response_model=list[schemas.BusinessHourOut])
def get_hours(db:Session=Depends(get_db),user=Depends(current_user)): return list(db.scalars(select(models.BusinessHour).where(models.BusinessHour.owner_id==user.id).order_by(models.BusinessHour.weekday)))
@app.put("/api/business-hours",response_model=list[schemas.BusinessHourOut])
def put_hours(data:list[schemas.BusinessHourIn],db:Session=Depends(get_db),user=Depends(current_user)):
    if len({x.weekday for x in data})!=len(data): raise HTTPException(400,"Dias duplicados")
    for x in data:
        if x.active and x.start_time>=x.end_time: raise HTTPException(400,"Horário inicial deve ser anterior ao final")
        obj=db.scalar(select(models.BusinessHour).where(models.BusinessHour.owner_id==user.id,models.BusinessHour.weekday==x.weekday))
        if obj:
            for k,v in x.model_dump().items(): setattr(obj,k,v)
        else: db.add(models.BusinessHour(**x.model_dump(),owner_id=user.id))
    db.commit(); return get_hours(db,user)
@app.get("/api/blocked-times",response_model=list[schemas.BlockedTimeOut])
def blocks(db:Session=Depends(get_db),user=Depends(current_user)): return list(db.scalars(select(models.BlockedTime).where(models.BlockedTime.owner_id==user.id).order_by(models.BlockedTime.date.desc())))
@app.post("/api/blocked-times",response_model=schemas.BlockedTimeOut,status_code=201)
def create_block(data:schemas.BlockedTimeIn,db:Session=Depends(get_db),user=Depends(current_user)):
    if data.start_time>=data.end_time: raise HTTPException(400,"Intervalo inválido")
    if data.professional_id: owned(models.Professional,data.professional_id,user,db)
    obj=models.BlockedTime(**data.model_dump(),owner_id=user.id); db.add(obj); db.commit(); db.refresh(obj); return obj
@app.put("/api/blocked-times/{item_id}",response_model=schemas.BlockedTimeOut)
def update_block(item_id:int,data:schemas.BlockedTimeIn,db:Session=Depends(get_db),user=Depends(current_user)):
    obj=owned(models.BlockedTime,item_id,user,db)
    if data.start_time>=data.end_time: raise HTTPException(400,"Intervalo inválido")
    for k,v in data.model_dump().items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj
@app.delete("/api/blocked-times/{item_id}",status_code=204)
def delete_block(item_id:int,db:Session=Depends(get_db),user=Depends(current_user)): db.delete(owned(models.BlockedTime,item_id,user,db)); db.commit()
@app.get("/api/appointments",response_model=list[schemas.AppointmentOut])
def appointments(start:date|None=None,end:date|None=None,professional_id:int|None=None,service_id:int|None=None,client_id:int|None=None,status:models.AppointmentStatus|None=None,db:Session=Depends(get_db),user=Depends(current_user)):
    q=select(models.Appointment).where(models.Appointment.owner_id==user.id)
    for cond in [models.Appointment.date>=start if start else None,models.Appointment.date<=end if end else None,models.Appointment.professional_id==professional_id if professional_id else None,models.Appointment.service_id==service_id if service_id else None,models.Appointment.client_id==client_id if client_id else None,models.Appointment.status==status if status else None]:
        if cond is not None: q=q.where(cond)
    return list(db.scalars(q.order_by(models.Appointment.date,models.Appointment.start_time)))
@app.get("/api/appointments/{item_id}",response_model=schemas.AppointmentOut)
def appointment(item_id:int,db:Session=Depends(get_db),user=Depends(current_user)): return owned(models.Appointment,item_id,user,db)
@app.post("/api/appointments",response_model=schemas.AppointmentOut,status_code=201)
def create_appointment(data:schemas.AppointmentIn,db:Session=Depends(get_db),user=Depends(current_user)):
    obj=models.Appointment(**validate_and_build(db,user.id,data)); db.add(obj); db.commit(); db.refresh(obj); return obj
@app.put("/api/appointments/{item_id}",response_model=schemas.AppointmentOut)
def update_appointment(item_id:int,data:schemas.AppointmentIn,db:Session=Depends(get_db),user=Depends(current_user)):
    obj=owned(models.Appointment,item_id,user,db)
    for k,v in validate_and_build(db,user.id,data,item_id).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj
@app.patch("/api/appointments/{item_id}/status",response_model=schemas.AppointmentOut)
def status_appointment(item_id:int,data:schemas.StatusIn,db:Session=Depends(get_db),user=Depends(current_user)):
    obj=owned(models.Appointment,item_id,user,db); obj.status=data.status; db.commit(); db.refresh(obj); return obj
@app.delete("/api/appointments/{item_id}",status_code=204)
def delete_appointment(item_id:int,db:Session=Depends(get_db),user=Depends(current_user)): db.delete(owned(models.Appointment,item_id,user,db)); db.commit()
def report_data(db,user,start,end):
    items=list(db.scalars(select(models.Appointment).where(models.Appointment.owner_id==user.id,models.Appointment.date.between(start,end))))
    completed=[x for x in items if x.status==models.AppointmentStatus.completed]
    return {"start":start,"end":end,"total":len(items),"completed":len(completed),"cancelled":sum(x.status==models.AppointmentStatus.cancelled for x in items),"no_show":sum(x.status==models.AppointmentStatus.no_show for x in items),"revenue":sum((x.price for x in completed),Decimal(0)),"clients_served":len({x.client_id for x in completed}),"services_performed":len(completed)}
@app.get("/api/dashboard")
def dashboard(db:Session=Depends(get_db),user=Depends(current_user)):
    today=date.today(); month=today.replace(day=1); data=report_data(db,user,month,today)
    data.update({"today":len(list(db.scalars(select(models.Appointment).where(models.Appointment.owner_id==user.id,models.Appointment.date==today)))),"upcoming":len(list(db.scalars(select(models.Appointment).where(models.Appointment.owner_id==user.id,models.Appointment.date>=today,models.Appointment.status.in_([models.AppointmentStatus.scheduled,models.AppointmentStatus.confirmed]))))),"clients":db.scalar(select(func.count()).select_from(models.Client).where(models.Client.owner_id==user.id)),"professionals":db.scalar(select(func.count()).select_from(models.Professional).where(models.Professional.owner_id==user.id)),"services":db.scalar(select(func.count()).select_from(models.Service).where(models.Service.owner_id==user.id))}); return data
@app.get("/api/reports/appointments")
def report_appointments(start:date=Query(default_factory=lambda:date.today().replace(day=1)),end:date=Query(default_factory=date.today),db:Session=Depends(get_db),user=Depends(current_user)): return report_data(db,user,start,end)
@app.get("/api/reports/revenue")
def report_revenue(start:date,end:date,db:Session=Depends(get_db),user=Depends(current_user)): return {"revenue":report_data(db,user,start,end)["revenue"]}
@app.get("/api/reports/services")
def report_services(start:date,end:date,db:Session=Depends(get_db),user=Depends(current_user)):
    rows=db.execute(select(models.Service.name,func.count(models.Appointment.id)).join(models.Appointment).where(models.Appointment.owner_id==user.id,models.Appointment.date.between(start,end),models.Appointment.status==models.AppointmentStatus.completed).group_by(models.Service.name)).all(); return [{"service":n,"total":c} for n,c in rows]
@app.get("/api/reports/cancellations")
def report_cancellations(start:date,end:date,db:Session=Depends(get_db),user=Depends(current_user)): return {k:v for k,v in report_data(db,user,start,end).items() if k in ("cancelled","no_show")}
