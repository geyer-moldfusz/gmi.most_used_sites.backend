from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
import hashlib


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unique_id = Column(String(24), unique=True)


class Visit(Base):
    __tablename__ = 'visits'
    id = Column(String(20), primary_key=True)
    url = Column(String(512), nullable=False)
    visited_at = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref='visits')

    def __init__(self, **kwargs):
        super(Visit, self).__init__(**kwargs)
        self.id = self._id()

    def _id(self):
        if not self.url:
            return  # XXX raise
        if not self.visited_at:
            return  # xxx raise
        sha1 = hashlib.sha1()
        sha1.update(self.url.encode())
        sha1.update(str(self.visited_at).encode())
        return sha1.hexdigest()
