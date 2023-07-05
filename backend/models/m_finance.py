from typing import Union, Optional
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy import String
from datetime import date
import os

b_name = os.path.split(__file__)[-1].split('.')[0]

class Base(DeclarativeBase):
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{b_name}_{cls.__name__.lower()}'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(default=date.today())


class Exchange(Base):
    group_source: Mapped[str] = mapped_column(nullable=True)
    source: Mapped[str]
    currency: Mapped[str]
    sales: Mapped[float]
    buy: Mapped[float]
    year: Mapped[int]
    month: Mapped[int]
    date: Mapped[date]


class NewsExchange(Base):
    email: Mapped[str]