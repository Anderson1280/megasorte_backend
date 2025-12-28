# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_premium = Column(Boolean, default=False)
    credits = Column(Integer, default=0)
    book_access = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plays = relationship("Play", back_populates="user")


class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    round_id = Column(Integer, nullable=False)
    numbers = Column(String, nullable=False)

    device_fp = Column(String)
    ip = Column(String)
    region = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="plays")

    __table_args__ = (
        UniqueConstraint("user_id", "round_id", name="uix_user_round"),
    )
