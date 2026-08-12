from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
import hashlib
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .config import settings
from .database import get_db
from .email_verification import generate_verification_token, hash_verification_token
from .mfa import create_mfa_setup, verify_totp
from .models import AuditEvent, EmailVerificationToken, RecoveryCode, Session, User
from .schemas import EmailVerificationRequest, LoginRequest, MessageResponse, RefreshRequest, RegisterRequest, ResendVerificationRequest, TokenResponse, UserResponse
from .security import create_access_token, create_refresh_token, decode_token, hash_password, hash_refresh_token, verify_password

app = FastAPI(title=settings.app_name, version="0.5.1")
bearer = HTTPBearer(auto_error=False)

def hash_recovery_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

@app.get("/health")
async def health() -> dict[str, str]: return {"status": "ok"}

async def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: AsyncSession = Depends(get_db)) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer": raise HTTPException(status_code=401, detail="Authentication required")
    try:
        claims = decode_token(credentials.credentials)
        if claims.get("type") != "access": raise ValueError("wrong token type")
        user_id, session_id = UUID(claims["sub"]), UUID(claims["sid"])
    except (ValueError, KeyError) as exc: raise HTTPException(status_code=401, detail="Invalid access token") from exc
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None or not user.is_active: raise HTTPException(status_code=401, detail="User inactive or not found")
    session = (await db.execute(select(Session).where(Session.id == session_id, Session.user_id == user_id))).scalar_one_or_none()
    if session is None or session.revoked_at is not None or session.expires_at <= datetime.now(timezone.utc): raise HTTPException(status_code=401, detail="Session expired or revoked")
    return user

async def _create_email_verification(user: User, db: AsyncSession) -> str:
    token, digest, expires_at = generate_verification_token()
    db.add(EmailVerificationToken(user_id=user.id, token_hash=digest, expires_at=expires_at))
    db.add(AuditEvent(actor_id=user.id, action="identity.email_verification.issued", resource_type="user", resource_id=str(user.id)))
    await db.commit()
    return token

@app.post("/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> User:
    email = payload.email.lower()
    if (await db.execute(select(User).where(User.email == email))).scalar_one_or_none() is not None: raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=email, password_hash=hash_password(payload.password), display_name=payload.display_name)
    db.add(user); await db.flush(); db.add(AuditEvent(actor_id=user.id, action="identity.user.created", resource_type="user", resource_id=str(user.id)))
    await db.commit(); await db.refresh(user); await _create_email_verification(user, db)
    return user

@app.post("/v1/auth/verify-email", response_model=MessageResponse)
async def verify_email(payload: EmailVerificationRequest, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    now = datetime.now(timezone.utc)
    record = (await db.execute(select(EmailVerificationToken).where(EmailVerificationToken.token_hash == hash_verification_token(payload.token), EmailVerificationToken.used_at.is_(None)))).scalar_one_or_none()
    if record is None or record.expires_at <= now: raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    user = (await db.execute(select(User).where(User.id == record.user_id))).scalar_one_or_none()
    if user is None or not user.is_active: raise HTTPException(status_code=400, detail="User unavailable")
    record.used_at = now; user.email_verified = True
    db.add(AuditEvent(actor_id=user.id, action="identity.email_verification.completed", resource_type="user", resource_id=str(user.id)))
    await db.commit(); return MessageResponse(message="Email verified")

@app.post("/v1/auth/resend-verification", response_model=MessageResponse)
async def resend_verification(payload: ResendVerificationRequest, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    user = (await db.execute(select(User).where(User.email == payload.email.lower()))).scalar_one_or_none()
    if user is not None and user.is_active and not user.email_verified: await _create_email_verification(user, db)
    return MessageResponse(message="If the account requires verification, a new verification token has been issued")

@app.post("/v1/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = (await db.execute(select(User).where(User.email == payload.email.lower()))).scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash) or not user.is_active: raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.email_verified: raise HTTPException(status_code=403, detail="Email verification required")
    if user.mfa_enabled: raise HTTPException(status_code=403, detail="MFA verification required")
    return await _issue_session(user, db)

async def _issue_session(user: User, db: AsyncSession) -> TokenResponse:
    session_id = uuid4(); expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)
    refresh_token = create_refresh_token(str(user.id), str(session_id), expires_at)
    db.add(Session(id=session_id, user_id=user.id, refresh_token_hash=hash_refresh_token(refresh_token), expires_at=expires_at)); db.add(AuditEvent(actor_id=user.id, action="identity.user.login", resource_type="session", resource_id=str(session_id)))
    await db.commit()
    return TokenResponse(access_token=create_access_token(str(user.id), str(session_id)), refresh_token=refresh_token, expires_in=settings.access_token_minutes * 60, session_id=session_id)

@app.post("/v1/auth/mfa/setup")
async def mfa_setup(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)) -> dict[str, object]:
    if user.mfa_enabled: raise HTTPException(status_code=409, detail="MFA already enabled")
    setup = create_mfa_setup(user.email); user.mfa_secret = setup.secret
    for code in setup.recovery_codes: db.add(RecoveryCode(user_id=user.id, code_hash=hash_recovery_code(code)))
    db.add(AuditEvent(actor_id=user.id, action="identity.mfa.setup_started", resource_type="user", resource_id=str(user.id))); await db.commit()
    return {"otpauth_uri": setup.otpauth_uri, "recovery_codes": list(setup.recovery_codes)}

@app.post("/v1/auth/mfa/verify", response_model=MessageResponse)
async def mfa_verify(code: str, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)) -> MessageResponse:
    if not user.mfa_secret: raise HTTPException(status_code=400, detail="MFA setup required")
    if not verify_totp(user.mfa_secret, code): raise HTTPException(status_code=401, detail="Invalid MFA code")
    user.mfa_enabled = True; db.add(AuditEvent(actor_id=user.id, action="identity.mfa.enabled", resource_type="user", resource_id=str(user.id))); await db.commit()
    return MessageResponse(message="MFA enabled")

@app.post("/v1/auth/mfa/recovery", response_model=TokenResponse)
async def mfa_recovery(email: str, password: str, recovery_code: str, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = (await db.execute(select(User).where(User.email == email.lower()))).scalar_one_or_none()
    if user is None or not verify_password(password, user.password_hash) or not user.is_active: raise HTTPException(status_code=401, detail="Invalid credentials")
    row = (await db.execute(select(RecoveryCode).where(RecoveryCode.user_id == user.id, RecoveryCode.code_hash == hash_recovery_code(recovery_code), RecoveryCode.used_at.is_(None)))).scalar_one_or_none()
    if row is None: raise HTTPException(status_code=401, detail="Invalid or used recovery code")
    row.used_at = datetime.now(timezone.utc); db.add(AuditEvent(actor_id=user.id, action="identity.mfa.recovery_used", resource_type="user", resource_id=str(user.id))); await db.commit()
    return await _issue_session(user, db)

@app.post("/v1/auth/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    try:
        claims = decode_token(payload.refresh_token)
        if claims.get("type") != "refresh": raise ValueError("wrong token type")
        session_id, user_id = UUID(claims["sid"]), UUID(claims["sub"])
    except (ValueError, KeyError) as exc: raise HTTPException(status_code=401, detail="Invalid refresh token") from exc
    session = (await db.execute(select(Session).where(Session.id == session_id, Session.user_id == user_id))).scalar_one_or_none(); now = datetime.now(timezone.utc)
    if session is None or session.revoked_at is not None or session.expires_at <= now: raise HTTPException(status_code=401, detail="Session expired or revoked")
    if session.refresh_token_hash != hash_refresh_token(payload.refresh_token):
        session.revoked_at = now; db.add(AuditEvent(actor_id=user_id, action="identity.security.refresh_reuse", resource_type="session", resource_id=str(session_id))); await db.commit(); raise HTTPException(status_code=401, detail="Refresh token reuse detected")
    session.revoked_at = now; user = (await db.execute(select(User).where(User.id == user_id))).scalar_one(); return await _issue_session(user, db)

@app.get("/v1/me", response_model=UserResponse)
async def me(user: User = Depends(current_user)) -> User: return user

@app.post("/v1/auth/logout", response_model=MessageResponse)
async def logout(user: User = Depends(current_user), credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: AsyncSession = Depends(get_db)) -> MessageResponse:
    if credentials is None: raise HTTPException(status_code=401, detail="Authentication required")
    session_id = UUID(decode_token(credentials.credentials)["sid"]); session = (await db.execute(select(Session).where(Session.id == session_id, Session.user_id == user.id))).scalar_one_or_none()
    if session and session.revoked_at is None: session.revoked_at = datetime.now(timezone.utc); db.add(AuditEvent(actor_id=user.id, action="identity.user.logout", resource_type="session", resource_id=str(session_id))); await db.commit()
    return MessageResponse(message="Logged out")

@app.post("/v1/auth/logout-all", response_model=MessageResponse)
async def logout_all(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)) -> MessageResponse:
    now = datetime.now(timezone.utc); await db.execute(update(Session).where(Session.user_id == user.id, Session.revoked_at.is_(None)).values(revoked_at=now)); db.add(AuditEvent(actor_id=user.id, action="identity.user.logout_all", resource_type="user", resource_id=str(user.id))); await db.commit(); return MessageResponse(message="All sessions revoked")
