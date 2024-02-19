from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

HBNB_MYSQL_USER = os.environ('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = os.environ('HBNB_MYSQL_PWD')
HBNB_MYSQL_DB = os.environ('HBNB_MYSQL_DB')
HBNB_MYSQL_HOST = os.environ('HBNB_MYSQL_HOST')
HBNB_ENV = os.environ('HBNB_ENV')


Base = declarative_base()
metadata = MetaData()

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(f'mysql+mysqldb://{HBNB_MYSQL_USER}:\
            {HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}',
            pool_pre_ping=True)


        if HBNB_ENV == 'test':
            metadata.drop_all(self.__engine)




    def all(self, cls=None):
        all_objects = {}

        if cls is not None:
            instances = self.__session.query(cls).all()
            for instance in instances:
                all_objects.update({instance.to_dict()['__class__'] + '.' + instance.id: instance})

        else:
            from models.user import User
            from models.place import Place
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.review import Review

            all_cls = [User, Place, State, City, Amenity, Review]

            for _cls in all_cls:
                instances = self.__session.query(_cls).all()
                for instance in instances:
                    all_objects.update({instance.to_dict()['__class__'] + '.' + instance.id: instance})


        return all_objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.query(obj).delete()

    def reload(self):
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        # Base.metadata.create