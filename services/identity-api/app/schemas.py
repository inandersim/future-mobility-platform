from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=2, max_length=200)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    session_id: UUID

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    display_name: str
    is_active: bool
    email_verified: bool
    mfa_enabled: bool

class MessageResponse(BaseModel):
    message: str

class EmailVerificationRequest(BaseModel):
    token: str = Field(min_length=20, max_length=512)

class ResendVerificationRequest(BaseModel):
    email: EmailStr

class MFAChallengeRequest(BaseModel):
    email: EmailStr
    password: str
    code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=20, max_length=512)
    new_password: str = Field(min_length=12, max_length=128)
