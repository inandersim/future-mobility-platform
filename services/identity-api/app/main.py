from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import get_db
from .models import AuditEvent, Session, User
from .schemas import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse, UserResponse
from .security import create_access_token, create_refresh_token, decode_token, hash_password, hash_refresh_token, verify_password

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.email == payload.email.lower()))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        display_name=payload.display_name,
    )
    db.add(user)
    await db.flush()
    db.add(AuditEvent(actor_id=user.id, action="identity.user.created", resource_type="user", resource_id=str(user.id)))
    await db.commit()
    await db.refresh(user)
    return user


@app.post("/v1/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == payload.email.lower()))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    session_id = uuid4()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)
    refresh_token = create_refresh_token(str(user.id), str(session_id), expires_at)
    session = Session(
        id=session_id,
        user_id=user.id,
        refresh_token_hash=hash_refresh_token(refresh_token),
        expires_at=expires_at,
    )
    db.add(session)
    db.add(AuditEvent(actor_id=user.id, action="identity.user.login", resource_type="session", resource_id=str(session_id)))
    await db.commit()

    return TokenResponse(
        access_token=create_access_token(str(user.id), str(session_id)),
        refresh_token=refresh_token,
        expires_in=settings.access_token_minutes * 60,
        session_id=session_id,
    )


@app.post("/v1/auth/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        claims = decode_token(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

    if claims.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    session_id = UUID(claims["sid"])
    user_id = UUID(claims["sub"])
    result = await db.execute(select(Session).where(Session.id == session_id, Session.user_id == user_id))
    session = result.scalar_one_or_none()
    if session is None or session.revoked_at is not None or session.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired or revoked")
    if session.refresh_token_hash != hash_refresh_token(payload.refresh_token):
        session.revoked_at = datetime.now(timezone.utc)
        await db.commit()
        raise HTTPException(status_code=401, detail="Refresh token reuse detected")

    session.revoked_at = datetime.now(timezone.utc)
    new_session_id = uuid4()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)
    new_refresh = create_refresh_token(str(user_id), str(new_session_id), expires_at)
    db.add(Session(id=new_session_id, user_id=user_id, refresh_token_hash=hash_refresh_token(new_refresh), expires_at=expires_at))
    db.add(AuditEvent(actor_id=user_id, action="identity.session.rotated", resource_type="session", resource_id=str(new_session_id)))
    await db.commit()

    return TokenResponse(
        access_token=create_access_token(str(user_id), str(new_session_id)),
        refresh_token=new_refresh,
        expires_in=settings.access_token_minutes * 60,
        session_id=new_session_id,
    )
