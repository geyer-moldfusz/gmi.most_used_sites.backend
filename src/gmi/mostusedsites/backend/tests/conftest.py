from gmi.mostusedsites.backend.models import Base, Visit, User, DBSession
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from transaction import abort
from webtest import TestApp
import os
import pytest


TESTDB = 'test_project.db'
TESTDB_PATH = "/tmp/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def setup_app():
    config = Configurator(settings={})
    return config.make_wsgi_app()


@pytest.fixture(scope='session')
def app(setup_app):
    return TestApp(setup_app)

@pytest.fixture
def session(connection, request):
    trans = connection.begin()          # begin a non-orm transaction
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)
    return DBSession()

@pytest.fixture(scope='session')
def connection(app, request):
    """Session-wide test database."""
#    if os.path.exists(TESTDB_PATH):
#        os.unlink(TESTDB_PATH)
#
#    def teardown():
#        os.unlink(TESTDB_PATH)

    engine = create_engine('sqlite://')
    connection = engine.connect()
    DBSession.registry.clear()
    DBSession.configure(bind=connection)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

#    request.addfinalizer(teardown)
    return connection


#@pytest.yield_fixture(scope='function')
#def session(db, request):
#    """Creates a new database session for a test."""
#    connection = db.engine.connect()
#    transaction = connection.begin()
#
#    options = dict(bind=connection, binds={})
#    session = db.create_scoped_session(options=options)
#
#    db.session = session
#
#    yield session
#
#    transaction.rollback()
#    connection.close()
#    session.remove()


@pytest.fixture(scope='function')
def visits(session):
    user = User(unique_id='ujadkapdydazujuksyairpin')
    visit = Visit(url='test_visit', visited_at=1, duration=1, user=user)
    session.add(user)
    session.add(visit)
