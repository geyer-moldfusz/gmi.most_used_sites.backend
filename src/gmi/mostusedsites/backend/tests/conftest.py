from gmi.mostusedsites.backend.models import Base, DBSession, User, Visit
from sqlalchemy import create_engine
from webtest import TestApp
import gmi.mostusedsites.backend as backend
import pytest
import transaction


@pytest.fixture(scope="session")
def app(request):
    settings = {'sqlalchemy.url': 'sqlite:///:memory:'}
    app = TestApp(backend.main({}, **settings))
    Base.metadata.create_all()

    request.addfinalizer(Base.metadata.drop_all)
    return app


@pytest.fixture(scope="session")
def test_data(app):
    user = User(unique_id='ujadkapdydazujuksyairpin')
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
    DBSession.add_all(visits)
    transaction.commit()

    return {'visits': visits, 'users': [user]}


@pytest.fixture(scope="function")
def session(request, test_data):
    request.addfinalizer(DBSession.rollback)
    request.addfinalizer(DBSession.close)
    return DBSession
