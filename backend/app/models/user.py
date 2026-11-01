import uuid
import enum


from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Uuid,Boolean,DateTime,Enum,String,func
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship



class UserRole(str, enum.Enum):
    CANDIDATE = 'CANDIDATE'
    EMPLOYER = 'EMPLOYER'
    ADMIN = 'ADMIN'




class User(Base):

    __tablename__ = 'users'

    id:Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,

    )

    email:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )


    password_hash:Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )


    role:Mapped[UserRole] = mapped_column(

        Enum(
            UserRole,
            name="user_role",
            values_callable = lambda enum_cls:[member.value for member in enum_cls ],
    ),
            nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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

    candidate_profile = relationship(
        "CandidateProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    employer_profile = relationship(
        "EmployerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )



