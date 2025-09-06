from uuid import UUID as Py_UUID
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as Pg_UUID

from app.db.database import Base


class Tickets(Base):
    __tablename__ = "tickets"

    id: Mapped[Py_UUID] = mapped_column(
        Pg_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    subject: Mapped[str]
    course: Mapped[int]
    question: Mapped[str]
    answer: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        server_onupdate=text("TIMEZONE('utc', now())"),
    )
