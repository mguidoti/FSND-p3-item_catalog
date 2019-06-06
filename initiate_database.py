"""
Creates the database themehospitals.db
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# Creates an instance of the declarative_base class
Base = declarative_base()


class User(Base):
    # Sets table name
    __tablename__ = 'user'

    # Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    picture = Column(String(250))

    # Creates a serialization property to be used on the API endopoint
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'gender': self.gender,
            'email': self.email,
            'picture': self.picture,
            'type': self.type,
        }


class Hospital(Base):
    # Sets table name
    __tablename__ = 'hospital'

    # Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    accepted_insurance = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Creates a serialization property to be used on the API endopoint
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'accepted_insurance': self.accepted_insurance,
            'address': self.address,
            'phone': self.phone,
            'owner id': self.user_id,
        }


class Condition(Base):
    # Sets table name
    __tablename__ = 'condition'

    # Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    cause = Column(String(250), nullable=False)
    sympton = Column(String(250), nullable=False)
    cure = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    cost = Column(String(250), nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospital.id'))
    hospital = relationship(Hospital)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Creates a serialization property to be used on the API endopoint
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'cause': self.cause,
            'sympton': self.sympton,
            'cure': self.cure,
            'type': self.type,
            'cost': self.cost,
            'hospital id': self.hospital_id,
            'hospital owner id': self.user_id,
        }


# Initiates an engine for the databases
engine = create_engine('sqlite:///themehospitals.db')
# Bind the engine to the metadata of the Base class to access the
# declaratives in a DBSession instance
Base.metadata.create_all(engine)
