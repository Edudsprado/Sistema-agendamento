from datetime import date, datetime, time
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from app.models import AppointmentStatus
class ORM(BaseModel): model_config=ConfigDict(from_attributes=True)
class Register(BaseModel): name:str=Field(min_length=2,max_length=100); email:EmailStr; password:str=Field(min_length=8,max_length=128)
class Login(BaseModel): email:EmailStr; password:str
class UserOut(ORM): id:int; name:str; email:EmailStr; active:bool
class Token(BaseModel): access_token:str; token_type:str="bearer"; user:UserOut
class ClientIn(BaseModel): name:str=Field(min_length=2,max_length=120); phone:str|None=Field(None,max_length=30); email:EmailStr|None=None; notes:str|None=Field(None,max_length=2000); active:bool=True
class ClientOut(ClientIn,ORM): id:int; created_at:datetime
class ServiceIn(BaseModel): name:str=Field(min_length=2,max_length=120); description:str|None=Field(None,max_length=2000); duration_minutes:int=Field(gt=0,le=1440); price:Decimal=Field(ge=0); active:bool=True
class ServiceOut(ServiceIn,ORM): id:int
class ProfessionalIn(BaseModel): name:str=Field(min_length=2,max_length=120); phone:str|None=Field(None,max_length=30); email:EmailStr|None=None; notes:str|None=Field(None,max_length=2000); active:bool=True; service_ids:list[int]=[]
class ProfessionalOut(ORM): id:int; name:str; phone:str|None; email:EmailStr|None; notes:str|None; active:bool; services:list[ServiceOut]=[]
class BusinessHourIn(BaseModel): weekday:int=Field(ge=0,le=6); start_time:time; end_time:time; active:bool=True
class BusinessHourOut(BusinessHourIn,ORM): id:int
class BlockedTimeIn(BaseModel): professional_id:int|None=None; date:date; start_time:time; end_time:time; reason:str=Field(min_length=2,max_length=180)
class BlockedTimeOut(BlockedTimeIn,ORM): id:int
class AppointmentIn(BaseModel): client_id:int; service_id:int; professional_id:int; date:date; start_time:time; price:Decimal|None=Field(None,ge=0); notes:str|None=Field(None,max_length=2000)
class StatusIn(BaseModel): status:AppointmentStatus
class AppointmentOut(ORM):
    id:int; client_id:int; service_id:int; professional_id:int; date:date; start_time:time; end_time:time; status:AppointmentStatus; price:Decimal; notes:str|None; client:ClientOut; service:ServiceOut; professional:ProfessionalOut
