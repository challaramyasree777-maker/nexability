from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.employer_accessibility_capability import AvailabilityStatus

# -------------------------------------------------------------
# Employer Profile Schemas
# -------------------------------------------------------------


class EmployerProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    email: EmailStr
    full_name: str
    company_name: str
    email_domain: str
    website: str | None = None
    phone: str | None = None
    verification_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployerProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    company_name: str | None = Field(default=None, min_length=2, max_length=200)
    website: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)


# -------------------------------------------------------------
# Job Description Document Schemas
# -------------------------------------------------------------


class JobDocumentResponse(BaseModel):
    id: UUID
    employer_profile_id: UUID
    original_filename: str
    storage_path: str
    mime_type: str
    file_size_bytes: int
    status: str
    download_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobDocumentActionResponse(BaseModel):
    message: str
    document: JobDocumentResponse | None = None


# -------------------------------------------------------------
# Employer Accessibility Capability Schemas
# -------------------------------------------------------------


class EmployerAccessibilityCreate(BaseModel):
    category: str = Field(
        min_length=2,
        max_length=50,
        description="E.g. SCREEN_READER, CAPTIONS, WHEELCHAIR, INTERVIEW",
    )
    capability: str = Field(
        min_length=2, max_length=150, description="E.g. Screen-reader-compatible systems"
    )
    status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    details: str | None = Field(default=None, max_length=500)


class EmployerAccessibilityUpdate(BaseModel):
    category: str | None = Field(default=None, min_length=2, max_length=50)
    capability: str | None = Field(default=None, min_length=2, max_length=150)
    status: AvailabilityStatus | None = None
    details: str | None = Field(default=None, max_length=500)


class EmployerAccessibilityResponse(BaseModel):
    id: UUID
    employer_profile_id: UUID
    category: str
    capability: str
    status: AvailabilityStatus
    details: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
