import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.email_verification import EmailVerification


TICKET_EXPIRY_MINUTES = 10


def hash_ticket(ticket: str) -> str:
    return hashlib.sha256(ticket.encode()).hexdigest()


def create_verification_ticket(
    db: Session,
    email: str,
    purpose: str,
) -> str:
    email = email.strip().lower()

    ticket = secrets.token_urlsafe(32)

    record = EmailVerification(
        email=email,
        token_hash=hash_ticket(ticket),
        purpose=purpose,
        expires_at=datetime.now(timezone.utc)
        + timedelta(minutes=TICKET_EXPIRY_MINUTES),
    )

    db.add(record)
    db.commit()

    return ticket


def validate_verification_ticket(
    db: Session,
    email: str,
    purpose: str,
    ticket: str,
) -> EmailVerification:
    record = db.scalar(
        select(EmailVerification)
        .where(
            EmailVerification.email == email.strip().lower(),
            EmailVerification.token_hash == hash_ticket(ticket),
            EmailVerification.purpose == purpose,
            EmailVerification.consumed_at.is_(None),
        )
        .with_for_update()
    )

    now = datetime.now(timezone.utc)

    if record is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or already used verification ticket",
        )

    if record.expires_at <= now:
        raise HTTPException(
            status_code=400,
            detail="Verification ticket has expired",
        )

    # Mark as consumed, but do not commit here.
    # Registration will commit this together with account creation.
    record.consumed_at = now

    return record