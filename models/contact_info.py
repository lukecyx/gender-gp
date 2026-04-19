from typing import Optional

from sqlmodel import Field
from uuid_extensions import uuid7

from .mixins import TimestampMixin


class ContactInfo(TimestampMixin, table=True):
    __tablename__ = "contact_info"  # type: ignore[assignment]
    id: str = Field(default_factory=lambda: str(uuid7()), primary_key=True)
    phone_1: str
    phone_2: Optional[str] = Field(default=None, nullable=True)
    address_line_1: str
    address_line_2: Optional[str] = Field(default=None, nullable=True)
    address_line_3: Optional[str] = Field(default=None, nullable=True)
