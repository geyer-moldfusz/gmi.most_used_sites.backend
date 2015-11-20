from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime


Base = declarative_base()


class EveBase(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class User(EveBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unique_id = Column(String(80), unique=True)


class Site(EveBase):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    url = Column(String(512))
    visited = Column(Integer)
    duration = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, uselist=False)
