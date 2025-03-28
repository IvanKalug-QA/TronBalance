from sqlalchemy import String, Column, DateTime
from sqlalchemy.sql import func

from app.core.db import Base


class Wallet(Base):
    address = Column(String, nullable=False)
    created_at = Column(
        DateTime,
        server_default=func.now(),
        index=True,
        nullable=False)
