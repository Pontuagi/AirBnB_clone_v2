#!/usr/bin/python3
"""Defines the DBStorage engine."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        database = os.getenv('HBNB_MYSQL_DB')

        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )

    def all(self, cls=None):
        if cls is None:
            cls_list = [User, State, City, Amenity, Place, Review]
            result = {}
            for cls in cls_list:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    result[key] = obj
            return result
        else:
            objs = self.__session.query(cls).all()
            cls_objects = {}
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                cls_objects[key] = obj
            return cls_objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session.close_all()
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
