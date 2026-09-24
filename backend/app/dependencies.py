from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.security import decode_token
bearer=HTTPBearer()
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db)):
    try: user=db.get(User,decode_token(credentials.credentials))
    except Exception: user=None
    if not user or not user.active: raise HTTPException(401,"Sessão inválida ou expirada")
    return user
