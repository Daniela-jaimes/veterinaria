from enum import Enum as PyEnum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Única Base declarativa de todos los modelos (async)."""


def pg_enum(enum_cls: type[PyEnum], name: str) -> SQLEnum:
    
    return SQLEnum(
        enum_cls,
        name=name,
        values_callable=lambda e: [m.value for m in e],
        create_type=False,
    )