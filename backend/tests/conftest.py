import io
import uuid
import zipfile
from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate_profile import CandidateProfile
from app.models.employer_profile import EmployerProfile
from app.models.user import User, UserRole


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"


@pytest.fixture
def sample_docx_bytes() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>',
        )
        zf.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8"?><w:document></w:document>',
        )
    return buf.getvalue()


@pytest.fixture
def create_candidate(db_session: Session):
    created_users = []

    def _factory(name: str = "Test Candidate", email: str | None = None):
        user_email = email or f"candidate_{uuid.uuid4().hex[:8]}@example.com"
        user = User(
            email=user_email,
            password_hash=hash_password("CandidateTestPass123!"),
            role=UserRole.CANDIDATE,
            is_active=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        db_session.add(user)
        db_session.flush()

        profile = CandidateProfile(
            user_id=user.id,
            full_name=name,
            phone="+1234567890",
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(profile)

        created_users.append(user.id)
        token = create_access_token(user_id=str(user.id), role=user.role.value)
        headers = {"Authorization": f"Bearer {token}"}
        return {"user": user, "profile": profile, "token": token, "headers": headers}

    yield _factory

    # Teardown
    for uid in created_users:
        u = db_session.get(User, uid)
        if u:
            db_session.delete(u)
    db_session.commit()


@pytest.fixture
def create_employer(db_session: Session):
    created_users = []

    def _factory(
        name: str = "Test Employer",
        company: str = "Acme Inclusive Corp",
        email: str | None = None,
        verification_status: str = "PENDING",
    ):
        domain = f"corp{uuid.uuid4().hex[:6]}.com"
        user_email = email or f"employer@{domain}"
        user = User(
            email=user_email,
            password_hash=hash_password("EmployerTestPass123!"),
            role=UserRole.EMPLOYER,
            is_active=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        db_session.add(user)
        db_session.flush()

        profile = EmployerProfile(
            user_id=user.id,
            full_name=name,
            company_name=company,
            email_domain=domain,
            website=f"https://www.{domain}",
            phone="+1987654321",
            verification_status=verification_status,
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(profile)

        created_users.append(user.id)
        token = create_access_token(user_id=str(user.id), role=user.role.value)
        headers = {"Authorization": f"Bearer {token}"}
        return {"user": user, "profile": profile, "token": token, "headers": headers}

    yield _factory

    for uid in created_users:
        u = db_session.get(User, uid)
        if u:
            db_session.delete(u)
    db_session.commit()


@pytest.fixture
def create_admin(db_session: Session):
    created_users = []

    def _factory(email: str | None = None):
        user_email = email or f"admin_{uuid.uuid4().hex[:8]}@nexability.org"
        user = User(
            email=user_email,
            password_hash=hash_password("AdminTestPass123!"),
            role=UserRole.ADMIN,
            is_active=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        created_users.append(user.id)
        token = create_access_token(user_id=str(user.id), role=user.role.value)
        headers = {"Authorization": f"Bearer {token}"}
        return {"user": user, "token": token, "headers": headers}

    yield _factory

    for uid in created_users:
        u = db_session.get(User, uid)
        if u:
            db_session.delete(u)
    db_session.commit()
