from gmi.mostusedsites.backend.models import Base, Visit, User, DBSession
from pyramid.config import Configurator
from pyramid.testing import testConfig
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from transaction import abort
from webtest import TestApp
from gmi.mostusedsites.backend import main
import os
import pytest


@pytest.fixture(scope='session')
def setup_app():
    settings = { 'sqlalchemy.url': 'sqlite://' }
    return main({}, **settings)


@pytest.fixture(scope='session')
def app(setup_app):
    return TestApp(setup_app)


@pytest.yield_fixture(scope='class')
def connection(app, request):
    """Session-wide test database."""
    connection = Base.metadata.bind.connect()
    Base.metadata.create_all()

    yield connection

    Base.metadata.drop_all()


@pytest.fixture(scope='function')
def session(connection, request):
    trans = connection.begin()          # begin a non-orm transaction
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)

    return DBSession()


@pytest.fixture(scope='function')
def visits(session):
    user = User(unique_id='ujadkapdydazujuksyairpin')
    session.add(user)
    session.add(Visit(
        url='http://test_visit',
        visited_at=1,
        duration=1,
        user=user,
        active=True))
    session.add(Visit(
        url='http://test_visit/foo?bar',
        visited_at=1,
        duration=1,
        user=user,
        active=False))
