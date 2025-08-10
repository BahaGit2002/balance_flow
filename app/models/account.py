from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Account(Base):
    __tablename__ = "accounts"

    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        default=Decimal(0.00),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts",
        lazy="joined",
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="account",
        cascade="none",
        lazy="selectin",
    )
