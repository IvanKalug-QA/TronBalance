from sqlalchemy import String, Column

from app.core.db import Base


class Wallet(Base):
    address = Column(String, nullable=False)
