from sqlalchemy import (
    Table,
    Column,
    MetaData,
    String,
    Integer,
    BigInteger,
    DateTime,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


metadata = MetaData()

tickets_table = Table(
    "tickets",
    metadata,
    Column(
        "id",
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("subject", String, nullable=False),
    Column("course", Integer, nullable=False),
    Column("question", String, nullable=False),
    Column("answer", String, nullable=True),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
)

blacklist_table = Table(
    "blacklist",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=False),
)
