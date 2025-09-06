from datetime import datetime

from sqlalchemy import BigInteger, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Blacklist(Base):
    __tablename__ = "blacklist"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
