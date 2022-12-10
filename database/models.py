from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declarative_base, backref

Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    login = Column(String(120), nullable=False)
    hash = Column(String(255), nullable=False)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    birth_date = Column('birth_date', Date, nullable=True)
    work_place = Column(String(120), nullable=True)
    post_name = Column(String(120), nullable=True)
    phones = relationship('Phone', back_populates='person', cascade='all,delete')
    emails = relationship('Email', back_populates='person', cascade='all,delete')

    @hybrid_property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

    @hybrid_property
    def description(self):
        return "post: " + str(self.post_name) + ' at company: '\
               + str(self.work_place) + ". Birthday: "\
               + str(self.birth_date)

    def modify_name(self):
        self.first_name = f'пан {self.first_name}'
        return self.first_name


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone_number = Column('phone_number', String(120), nullable=False)
    description = Column('description', String(120), nullable=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"))
    person = relationship(Person, cascade='all,delete')


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column('phone_number', String(120), nullable=False)
    description = Column('description', String(120), nullable=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"))
    person = relationship(Person, cascade='all,delete')


@listens_for(Person, "before_insert")
def my_on_connect(mapper, connect, target: Person):
    target.modify_name()
