import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AvailabilityStatus(enum.StrEnum):
    AVAILABLE = "AVAILABLE"
    ON_REQUEST = "ON_REQUEST"
    UNAVAILABLE = "UNAVAILABLE"


class EmployerAccessibilityCapability(Base):
    __tablename__ = "employer_accessibility_capabilities"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    employer_profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("employer_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    capability: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    status: Mapped[AvailabilityStatus] = mapped_column(
        Enum(
            AvailabilityStatus,
            name="availability_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=AvailabilityStatus.AVAILABLE,
        nullable=False,
    )

    details: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    employer_profile = relationship(
        "EmployerProfile",
        back_populates="accessibility_capabilities",
    )
