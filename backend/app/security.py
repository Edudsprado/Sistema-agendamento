from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()
_revoked_tokens: dict[str, datetime] = {}


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def _clear_expired_revocations() -> None:
    now = datetime.now(timezone.utc)
    expired = [jti for jti, exp in _revoked_tokens.items() if exp <= now]
    for jti in expired:
        _revoked_tokens.pop(jti, None)


def create_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expires, "jti": uuid4().hex}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_payload(token: str) -> dict:
    _clear_expired_revocations()
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    jti = payload.get("jti")
    if jti and jti in _revoked_tokens:
        raise jwt.InvalidTokenError("Token revogado")
    return payload


def decode_token(token: str) -> int:
    return int(decode_payload(token)["sub"])


def revoke_token(token: str) -> None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return

    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        return

    _clear_expired_revocations()
    _revoked_tokens[jti] = datetime.fromtimestamp(exp, tz=timezone.utc)
