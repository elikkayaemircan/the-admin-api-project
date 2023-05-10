from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class HOST(Base):
    __tablename__ = "V_HOST"
    __table_args__ = {"schema": "S_HOST"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(String)
    STATUS = Column(String)
    ADMIN = Column(String, nullable=True)
    CRITICAL = Column(Boolean)
