from typing import List, Optional, Union

from app.crud import SLUGTYPE, BaseCRUD
from app.utils import unique_slug_generator
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.contact.models import Contact
from app.contact.schemas import ContactCreate


class ContactCRUD(BaseCRUD[Contact, ContactCreate, ContactCreate, SLUGTYPE]):
    
    def create(self, obj_in: ContactCreate) -> Contact:
        Contact.objects.create(**obj_in.dict())
        return {"detail": "Message sent successfully!" }
    
contact = ContactCRUD(Contact)
