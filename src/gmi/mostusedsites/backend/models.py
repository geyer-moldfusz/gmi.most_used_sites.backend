from sqlalchemy import (
    Column, String, BigInteger, Integer, ForeignKey, DateTime, Boolean)
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
import hashlib

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unique_id = Column(String(24), unique=True)


class Visit(Base):
    __tablename__ = 'visits'
    id = Column(String(40), primary_key=True)
    url = Column(String(512), nullable=False)
    visited_at = Column(BigInteger, nullable=False)
    duration = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)
    scheme = Column(String(32), nullable=False)
    host = Column(String(512), nullable=False)
    path = Column(String(512), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref='visits')

    def __init__(self, url, **kwargs):
        self.url = url              # XXX this should be obsolete in future
        super(Visit, self).__init__(**kwargs)
        self.id = self._id()        # use multicolumn uniqueness
        self.scheme, self.host, self.path = self._url(url)

    def _id(self):
        if not self.url:
            return  # XXX raise
        if not self.visited_at:
            return  # xxx raise
        sha1 = hashlib.sha1()
        sha1.update(self.url.encode())
        sha1.update(str(self.visited_at).encode())
        return sha1.hexdigest()

    def _url(self, url):
        url = urlparse(url)
        return (url.scheme, url.netloc, url.path)
