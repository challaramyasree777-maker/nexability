"""Import model modules here when they are added so Alembic can discover metadata."""

from app.models.user import User, UserRole
from app.models.candidate_profile import CandidateProfile
from app.models.employer_profile import EmployerProfile
from app.models.candidate_declaration import CandidateDeclaration
from app.models.accommodation_preference import AccommodationPreference
from app.models.email_otp import EmailOTP
from app.models.email_verification import EmailVerification
from app.models.refresh_token import RefreshToken
from app.models.resume import Resume
from app.models.job_document import JobDocument
from app.models.employer_accessibility_capability import (
    EmployerAccessibilityCapability,
    AvailabilityStatus,
)

__all__ = [
    "User",
    "UserRole",
    "CandidateProfile",
    "EmployerProfile",
    "CandidateDeclaration",
    "AccommodationPreference",
    "EmailOTP",
    "EmailVerification",
    "RefreshToken",
    "Resume",
    "JobDocument",
    "EmployerAccessibilityCapability",
    "AvailabilityStatus",
]
