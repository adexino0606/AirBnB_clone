#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity

classes = {"User": User, "State": State, "City": City, "Amenity": Amenity,
           "Place": Place, "Review": Review}


class DBStorage:
    """Class for create New Engine"""

    __engine = None
    __session = None

    def __init__(self):

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      getenv('HBNB_MYSQL_USER'),
                                      getenv('HBNB_MYSQL_PWD'),
                                      getenv('HBNB_MYSQL_HOST'),
                                      getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if (getenv('HBNB_ENV')) == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        all_dict = {}
        if (cls is None):
            for v in classes.values():
                result = self.__session.query(v).all()
                for row in result:
                    key_dict = row.__class__.__name__ + '.' + row.id
                    all_dict[key_dict] = row
        else:
            result = self.__session.query(cls).all()
            for row in result:
                key_dict = row.__class__.__name__ + '.' + row.id
                all_dict[key_dict] = row

        return (all_dict)

    def new(self, obj):
        """add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """ delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_f = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_f)
        self.__session = Session
