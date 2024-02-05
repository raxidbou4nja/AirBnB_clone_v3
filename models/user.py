#!/usr/bin/python3
""" Holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def save(self):
        """Save the User instance."""
        if not self.id:
            self.password = hashlib.md5(self.password.encode()).hexdigest()
        super().save()

    def to_dict(self, save_to_disk=False):
        """Convert instance attributes to dictionary for JSON serialization."""
        new_dict = super().to_dict(save_to_disk)
        if not save_to_disk:
            new_dict.pop('password', None)
        return new_dict
