from sqlmodel import Session

from models.contact_info import ContactInfo


class ContactInfoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, contact_info: ContactInfo) -> ContactInfo:
        self.session.add(contact_info)
        self.session.commit()
        self.session.refresh(contact_info)

        return contact_info
