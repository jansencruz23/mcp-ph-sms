from typing import List, Optional
from sqlmodel import Session, select, col
from datetime import datetime
from .models import Contact, SMSLog
from .database import engine


class ContactRepository:
    def create(self, name: str, phone: str, tags: List[str], notes: str) -> Contact:
        with Session(engine) as session:
            contact = Contact(name=name, phone=phone, notes=notes)
            contact.tags_list = tags
            session.add(contact)
            session.commit()
            session.refresh(contact)
            return contact

    def get(self, contact_id: int) -> Optional[Contact]:
        with Session(engine) as session:
            return session.get(Contact, contact_id)

    def get_by_phone(self, phone: str) -> Optional[Contact]:
        with Session(engine) as session:
            statement = select(Contact).where(Contact.phone == phone)
            return session.exec(statement).first()

    def list(self, limit: int = 50, tag: str = None, q: str = None) -> List[Contact]:
        with Session(engine) as session:
            statement = select(Contact)
            if tag:
                statement = statement.where(col(Contact._tags).contains(tag))
            if q:
                statement = statement.where(
                    (col(Contact.name).contains(q)) | (col(Contact.phone).contains(q))
                )
            statement = statement.limit(limit)
            return session.exec(statement).all()

    def update(self, contact_id: int, **kwargs) -> Optional[Contact]:
        with Session(engine) as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                return None

            for key, value in kwargs.items():
                if key == "tags":
                    contact.tags_list = value
                elif hasattr(contact, key):
                    setattr(contact, key, value)

            contact.updated_at = datetime.utcnow()
            session.add(contact)
            session.commit()
            session.refresh(contact)
            return contact

    def delete(self, contact_id: int) -> bool:
        with Session(engine) as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                return False

            session.delete(contact)
            session.commit()
            return True


class SMSRepository:
    def log(
        self,
        recipient: str,
        message: str,
        status: str,
        response_code: int = None,
        contact_id: int = None,
    ):
        with Session(engine) as session:
            log_entry = SMSLog(
                recipient_phone=recipient,
                message=message,
                status=status,
                response_code=response_code,
                contact_id=contact_id,
            )
            session.add(log_entry)
            session.commit()

    def list(self, limit: int = 50, contact_id: int = None) -> List[SMSLog]:
        with Session(engine) as session:
            statement = select(SMSLog)
            if contact_id:
                statement = statement.where(SMSLog.contact_id == contact_id)
            statement = statement.order_by(SMSLog.timestamp.desc()).limit(limit)
            return session.exec(statement).all()
