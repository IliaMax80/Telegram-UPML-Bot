import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base_model import BaseModel


class Laundry(BaseModel):
    __tablename__ = 'laundries'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        unique=True, nullable=False,
    )

    # Когда был запущен таймер
    start_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
    # Когда он должен закончится
    end_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
    # Сколько раз было уведомление
    rings: Mapped[int] = mapped_column(
        Integer,
        nullable=True, default=0,
    )
    # Активен ли таймер
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True, default=False,
    )

    user = relationship('User', back_populates='laundry', lazy='selectin')
