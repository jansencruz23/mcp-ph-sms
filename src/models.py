from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field


class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str = Field(unique=True, index=True)
    tags: str = Field(default="", sa_column_kwargs={"name": "tags"})
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def tags_list(self) -> List[str]:
        return [t for t in self.tags.split(",") if t] if self.tags else []

    @tags_list.setter
    def tags_list(self, value: List[str]):
        self.tags = ",".join(value) if value else ""


class SMSLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    recipient_phone: str
    message: str
    status: str
    response_code: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
