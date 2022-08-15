#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """

    if models.storage_type == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all")
    else:
        name = ""

        @property
        def cities(self):
            new_list = []
            cities_all = models.storage.all(City)
            for value in cities_all.values():
                if (value.state_id == self.id):
                    new_list.append(value)
            return new_list
