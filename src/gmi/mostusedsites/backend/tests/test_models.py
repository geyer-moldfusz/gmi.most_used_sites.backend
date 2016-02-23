from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from gmi.mostusedsites.backend.models import Base, User, Visit
import pytest


class TestModels:
    def test_user(self, session):
        user = User(unique_id='foo')
        session.add(user)
        assert session.flush() is None

    def test_user_id_is_unique(self, session):
        user = User(unique_id='bar')
        user2 = User(unique_id='bar')
        session.add(user)
        session.add(user2)

        with pytest.raises(IntegrityError):
            session.flush()

    def test_visit(self, session):
        visit = Visit('http://foo', visited_at=1, duration=1, active=True)
        session.add(visit)
        assert session.flush() is None

    def test_visit_belongs_to_user(self):
        user = User(unique_id='foo')
        visit = Visit('http://foo', visited_at=1, duration=1, active=True)
        user.visits.append(visit)

        assert visit.user is user

    def test_visit_url_is_present(self):
        with pytest.raises(TypeError):
            visit = Visit(visited_at=1, duration=1, active=True)

    def test_visit_visited_at_is_present(self, session):
        visit = Visit('http://foo_visited', duration=1, active=True)
        session.add(visit)

        with pytest.raises(IntegrityError):
            session.flush()

    def test_visit_duration_is_present(self, session):
        visit = Visit('http://foo_duration', visited_at=1, active=True)
        session.add(visit)

        with pytest.raises(IntegrityError):
            session.flush()

    def test_visit_active_is_present(self, session):
        visit = Visit('http://foo_active', duration=1, visited_at=1)
        session.add(visit)

        with pytest.raises(IntegrityError):
            session.flush()

    def test_visit_id(self):
        visit = Visit('http://foo', visited_at=1, duration=1)
        assert visit.id == '1aa0598ba12ba82e6b6a88f97f010948f33a01d5'

    def test_visit_id_unique(self, session):
        visit = Visit('http://bar', visited_at=1, duration=1)
        visit1 = Visit(url='http://bar', visited_at=1, duration=1)
        session.add(visit)
        session.add(visit1)

        with pytest.raises(IntegrityError):
            session.flush()

    def test_visit_id_long_timestamp(self):
        visit = Visit("http://bar", visited_at=1449073100894, duration=1)
        assert visit.id == 'cdd896d38b96f973e2d0f446daf5da090878f585'

    def test_visit_schema(self):
        visit = Visit('https://bar', visited_at=1, duration=1)
        assert visit.scheme == 'https'

    def test_visit_host(self):
        visit = Visit('https://bar', visited_at=1, duration=1)
        assert visit.host == 'bar'

    def test_visit_path(self):
        visit = Visit('https://bar/foo/baz', visited_at=1, duration=1)
        assert visit.path == '/foo/baz'

    def test_visit_no_params(self):
        visit = Visit('https://bar/foo?a=1&b=2', visited_at=1, duration=1)
        assert visit.path == '/foo'
