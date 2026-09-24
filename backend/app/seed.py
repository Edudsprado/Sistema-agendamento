from datetime import time
from decimal import Decimal
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Client, Professional, Service, User
from app.security import hash_password

def run():
    with SessionLocal() as db:
        if db.scalar(select(User).where(User.email=="admin@agendapro.local")): return
        user=User(name="Administrador",email="admin@agendapro.local",password_hash=hash_password("Agenda123!")); db.add(user); db.flush()
        services=[Service(owner_id=user.id,name="Corte",description="Corte profissional",duration_minutes=30,price=Decimal("45")),Service(owner_id=user.id,name="Barba",description="Modelagem",duration_minutes=30,price=Decimal("35"))]
        db.add_all(services); db.flush(); pro=Professional(owner_id=user.id,name="Carlos Silva",phone="(65) 99999-1000",active=True); pro.services=services; db.add(pro); db.add(Client(owner_id=user.id,name="Marina Costa",phone="(65) 99999-2000",email="marina@example.com")); db.commit()
if __name__=="__main__": run()
