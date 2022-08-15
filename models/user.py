#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if models.storage_type == 'db':
        __tablename__ = "users"
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        places = relationship("Place", backref="user", cascade='all')
        reviews = relationship("Review", backref="user", cascade='all')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
