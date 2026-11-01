from pydantic import BaseModel, EmailStr, Field


class EmployerEmailCheckRequest(BaseModel):
    email: EmailStr


class EmployerEmailCheckResponse(BaseModel):
    eligible: bool
    reason: str
    domain: str | None = None




from typing import Literal

from pydantic import BaseModel, EmailStr


OTPPurpose = Literal[
    "CANDIDATE_REGISTRATION",
    "EMPLOYER_REGISTRATION",
    "PASSWORD_RESET",
]


class OTPSendRequest(BaseModel):
    email: EmailStr
    purpose: OTPPurpose


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    purpose: OTPPurpose
    otp: str


class OTPResponse(BaseModel):
    message: str
    expires_in: int | None = None

class OTPVerifyResponse(BaseModel):
    verified: bool
    message: str
    verification_ticket: str
    expires_in: int




class CandidateRegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=20)
    verification_ticket: str = Field(min_length=20)


class CandidateRegisterResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    message: str



class EmployerRegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    company_name: str = Field(min_length=2, max_length=200)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=20)
    website: str | None = Field(default=None, max_length=255)
    verification_ticket: str = Field(min_length=20)


class EmployerRegisterResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    company_name: str
    role: str
    verification_status: str
    message: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseModel):
    message: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    verification_ticket: str = Field(min_length=20)
    new_password: str = Field(min_length=8, max_length=128)

class GoogleLoginRequest(BaseModel):
    credential: str = Field(min_length=20)

