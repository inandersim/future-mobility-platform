from __future__ import annotations

import base64
import io
import secrets
from dataclasses import dataclass

import pyotp
import qrcode


@dataclass(frozen=True)
class MFASetup:
    secret: str
    otpauth_uri: str
    recovery_codes: tuple[str, ...]


def create_mfa_setup(email: str, issuer: str = "APEX") -> MFASetup:
    secret = pyotp.random_base32()
    uri = pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name=issuer)
    codes = tuple(secrets.token_hex(8) for _ in range(10))
    return MFASetup(secret=secret, otpauth_uri=uri, recovery_codes=codes)


def verify_totp(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def qr_png_base64(otpauth_uri: str) -> str:
    image = qrcode.make(otpauth_uri)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
