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
        visit = Visit(url='foo', visited_at=1, duration=1)
        session.add(visit)
        assert(commit() == None)

    def test_visit_belongs_to_user(self, session):
        user = User(unique_id='foo')
        visit = Visit(url='foo', visited_at=1, duration=1)
        user.visits.append(visit)

        assert(visit.user == user)

    def test_visit_url_is_present(self, session):
        visit = Visit(visited_at=1, duration=1)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_visited_at_is_present(self, session):
        visit = Visit(url='foo', duration=1)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_duration_is_present(self, session):
        visit = Visit(url='foo', visited_at=1)
        session.add(visit)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_id(self, session):
        visit = Visit(url='foo', visited_at=1, duration=1)
        assert(visit.id == '18a16d4530763ef43321d306c9f6c59ffed33072')

    def test_visit_id_unique(self, session):
        visit = Visit(url='bar', visited_at=1, duration=1)
        visit1 = Visit(url='bar', visited_at=1, duration=1)
        session.add(visit)
        session.add(visit1)

        with pytest.raises(IntegrityError):
            commit()

    def test_visit_id_long_timestamp(self, session):
        visit = Visit(url="bar", visited_at=1449073100894, duration=1)
        assert(visit.id == '33ad6c7d92b8944470d5ca8e9d897fb2f32376ae')
