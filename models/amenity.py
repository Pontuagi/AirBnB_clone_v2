#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from os import getenv
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """ A class representing amenity in mysql database """
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = relationship("Place", secondary=place_amenity,
                                       viewonly=False)
