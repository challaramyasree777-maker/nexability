from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# -------------------------------------------------------------
# Candidate Profile Schemas
# -------------------------------------------------------------


class CandidateProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    email: EmailStr
    full_name: str
    phone: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone: str | None = Field(default=None, max_length=20)


# -------------------------------------------------------------
# Resume Schemas
# -------------------------------------------------------------


class ResumeMetadataResponse(BaseModel):
    id: UUID
    candidate_profile_id: UUID
    original_filename: str
    storage_path: str
    mime_type: str
    file_size_bytes: int
    is_active: bool
    download_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeActionResponse(BaseModel):
    message: str
    resume: ResumeMetadataResponse | None = None


# -------------------------------------------------------------
# Candidate Accessibility Preference Schemas
# -------------------------------------------------------------


class AccessibilityPreferenceCreate(BaseModel):
    category: str = Field(
        min_length=2,
        max_length=50,
        description="E.g. SCREEN_READER, CAPTIONS, MOBILITY, TIME, REMOTE",
    )
    preference: str = Field(
        min_length=2, max_length=150, description="Specific accommodation needed"
    )
    details: str | None = Field(
        default=None,
        max_length=500,
        description="Optional extra details (do not disclose medical diagnosis)",
    )
    is_active: bool = True


class AccessibilityPreferenceUpdate(BaseModel):
    category: str | None = Field(default=None, min_length=2, max_length=50)
    preference: str | None = Field(default=None, min_length=2, max_length=150)
    details: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


class AccessibilityPreferenceResponse(BaseModel):
    id: UUID
    candidate_profile_id: UUID
    category: str
    preference: str
    details: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
