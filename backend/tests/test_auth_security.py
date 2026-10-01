import jwt


def test_protected_endpoint_requires_token(client):
    response = client.get("/api/dashboard")
    assert response.status_code in (401, 403)


def test_invalid_token_is_rejected(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer token-invalido"})
    assert response.status_code == 401


def test_logout_revokes_token(client, auth):
    assert client.get("/api/auth/me", headers=auth).status_code == 200
    assert client.post("/api/auth/logout", headers=auth).status_code == 204
    assert client.get("/api/auth/me", headers=auth).status_code == 401


def test_login_rate_limit_after_repeated_failures(client, auth):
    payload = {"email": "teste@example.com", "password": "senha-errada"}

    statuses = [client.post("/api/auth/login", json=payload).status_code for _ in range(6)]

    assert statuses[:5] == [401, 401, 401, 401, 401]
    assert statuses[5] == 429


def test_login_rejects_oversized_password(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "teste@example.com", "password": "a" * 129},
    )

    assert response.status_code == 422
