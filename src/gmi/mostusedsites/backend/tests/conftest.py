from gmi.mostusedsites.backend.models import (
    Base, Visit, User, State, DBSession)
from gmi.mostusedsites.backend import main
from pyramid.config import Configurator
from pyramid.testing import testConfig
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from transaction import abort
from webtest import TestApp
import os
import pytest


@pytest.fixture(scope='session')
def app():
    settings = { 'sqlalchemy.url': 'sqlite://' }
    return TestApp(main({}, **settings))


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
def user(session):
    user = User(unique_id='ujadkapdydazujuksyairpin')
    session.add(user)
    session.flush()

    return user


@pytest.fixture(scope='function')
def visits(session, user):
    visits = (
        Visit(
            url='http://test_visit',
            visited_at=1,
            duration=1,
            user=user,
            active=True),
        Visit(
            url='https://test_visit/foo?bar',
            visited_at=3,
            duration=1,
            user=user,
            active=False))
    session.add_all(visits)
    session.flush()

    return visits


@pytest.fixture(scope='function')
def status_intact(session):
    state = State(intact=True)
    session.add(state)


@pytest.fixture(scope='function')
def status_failure(session):
    state = State(intact=False)
    session.add(state)
