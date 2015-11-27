from sqlalchemy.exc import IntegrityError
from gmi.mostusedsites.backend.models import User, Visit
from transaction import commit
import pytest


class TestModels:
    def test_user(self, session):
        user = User(unique_id='foo')
        session.add(user)
        assert(commit() == None)

    def test_user_id_is_unique(self, session):
        user = User(unique_id='bar')
        user2 = User(unique_id='bar')
        session.add(user)
        session.add(user2)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit(self, session):
        visit = Visit(url='http://foo', visited_at=1, duration=1, active=True)
        session.add(visit)
        assert(commit() == None)

    def test_visit_belongs_to_user(self, session):
        user = User(unique_id='foo')
        visit = Visit(url='http://foo', visited_at=1, duration=1, active=True)
        user.visits.append(visit)

        assert(visit.user == user)

    def test_visit_url_is_present(self, session):
        visit = Visit(visited_at=1, duration=1, active=True)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_visited_at_is_present(self, session):
        visit = Visit(url='http://foo_visited', duration=1, active=True)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_duration_is_present(self, session):
        visit = Visit(url='http://foo_duration', visited_at=1, active=True)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_active_is_present(self, session):
        visit = Visit(url='http://foo_active', duration=1, visited_at=1)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_id(self, session):
        visit = Visit(url='http://foo', visited_at=1, duration=1)
        assert(visit.id == '1d112124d4e1fc9c9f0695bd7bfb346019a443a8')

    def test_visit_id_unique(self, session):
        visit = Visit(url='http://bar', visited_at=1, duration=1)
        visit1 = Visit(url='http://bar', visited_at=1, duration=1)
        session.add(visit)
        session.add(visit1)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_schema(self, session):
        visit = Visit(url='https://bar', visited_at=1, duration=1)
        assert(visit.scheme == 'https')
