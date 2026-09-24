import os
os.environ["DATABASE_URL"]="sqlite:///./test_agendapro.db"
os.environ["SECRET_KEY"]="test-secret-only"
import pytest
from fastapi.testclient import TestClient
from app.database import Base,engine
from app.main import app
@pytest.fixture(autouse=True)
def database():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine); yield; Base.metadata.drop_all(engine)
@pytest.fixture
def client(): return TestClient(app)
@pytest.fixture
def auth(client):
    r=client.post("/api/auth/register",json={"name":"Teste","email":"teste@example.com","password":"Senha123!"}); assert r.status_code==201
    return {"Authorization":f"Bearer {r.json()['access_token']}"}
