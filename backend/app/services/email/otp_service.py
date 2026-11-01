import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.email_otp import EmailOTP
from app.services.email.email_service  import send_otp_email


OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


def hash_otp(email: str, purpose: str, otp: str) -> str:
    secret = settings.OTP_HASH_SECRET

    if not secret:
        raise RuntimeError("OTP_HASH_SECRET is not configured")

    message = f"{email}:{purpose}:{otp}".encode()

    return hmac.new(
        secret.encode(),
        message,
        hashlib.sha256,
    ).hexdigest()


def send_otp(db: Session, email: str, purpose: str) -> None:
    email = email.strip().lower()

    # Invalidate previous unused OTPs for this email and purpose.
    now = datetime.now(timezone.utc)

    previous_otps = db.scalars(
        select(EmailOTP).where(
            EmailOTP.email == email,
            EmailOTP.purpose == purpose,
            EmailOTP.consumed_at.is_(None),
        )
    ).all()

    for previous in previous_otps:
        previous.consumed_at = now

    # Generate a cryptographically secure six-digit OTP.
    otp = f"{secrets.randbelow(1_000_000):06d}"

    record = EmailOTP(
        email=email,
        code_hash=hash_otp(email, purpose, otp),
        purpose=purpose,
        expires_at=now + timedelta(minutes=OTP_EXPIRY_MINUTES),
    )

    db.add(record)
    db.commit()

    try:
        send_otp_email(email, otp)
    except Exception:
        record.consumed_at = datetime.now(timezone.utc)
        db.commit()
        raise


def verify_otp(
    db: Session,
    email: str,
    purpose: str,
    otp: str,
) -> bool:
    email = email.strip().lower()

    record = db.scalar(
        select(EmailOTP)
        .where(
            EmailOTP.email == email,
            EmailOTP.purpose == purpose,
            EmailOTP.consumed_at.is_(None),
        )
        .order_by(EmailOTP.created_at.desc())
        .limit(1)
    )

    if record is None:
        raise HTTPException(400, "OTP not found or already used")

    now = datetime.now(timezone.utc)

    if record.expires_at <= now:
        record.consumed_at = now
        db.commit()
        raise HTTPException(400, "OTP has expired")

    if record.attempts >= MAX_OTP_ATTEMPTS:
        record.consumed_at = now
        db.commit()
        raise HTTPException(429, "Maximum OTP attempts exceeded")

    expected_hash = hash_otp(email, purpose, otp)

    if not hmac.compare_digest(record.code_hash, expected_hash):
        record.attempts += 1

        if record.attempts >= MAX_OTP_ATTEMPTS:
            record.consumed_at = now

        db.commit()
        raise HTTPException(400, "Invalid OTP")

    record.consumed_at = now
    db.commit()

    return True