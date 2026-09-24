from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import settings
password_hash=PasswordHash.recommended()
def hash_password(password:str)->str: return password_hash.hash(password)
def verify_password(password:str, hashed:str)->bool: return password_hash.verify(password,hashed)
def create_token(user_id:int)->str:
    expires=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":str(user_id),"exp":expires},settings.secret_key,algorithm="HS256")
def decode_token(token:str)->int:
    return int(jwt.decode(token,settings.secret_key,algorithms=["HS256"])["sub"])
