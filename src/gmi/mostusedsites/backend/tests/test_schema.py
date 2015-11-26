from gmi.mostusedsites.backend.schemas import (
    VisitsSchema,
    VisitSchema,
    UserSchema)
import colander
import pytest


class TestUserSchema:
    def test_valid(self):
        data = 'hegfejOsBuaKnignungOjEt4'
        des = UserSchema().deserialize(data)
        assert des == data

    def test_to_short(self):
        data = 'hegfejOsBuaKnignungOjEt'
        with pytest.raises(colander.Invalid):
            UserSchema().deserialize(data)

    def test_to_long(self):
        data = 'PopawhabKiarnalgejewsopsi'
        with pytest.raises(colander.Invalid):
            UserSchema().deserialize(data)

    def test_invalid(self):
        data = 'hegfejOsBua#nignungOjEt4'
        with pytest.raises(colander.Invalid):
            UserSchema().deserialize(data)


class TestVisitsSchema:
    def test_valid(self):
        data = [{'url': 'foo', 'duration': 1, 'visited_at': 1}]
        des = VisitsSchema().deserialize(data)
        assert des == data

    def test_no_list(self):
        data = dict(visits=dict(url='foo', duration=1, visited_at=1))
        with pytest.raises(colander.Invalid):
            VisitsSchema().deserialize(data)

    def test_no_dict(self):
        data = dict(url='foo', duration=1, visited_at=1)
        with pytest.raises(colander.Invalid):
            VisitsSchema().deserialize(data)


class TestVisitSchema:
    def test_valid(self):
        data = dict(url='foo', duration=1, visited_at=1)
        des = VisitSchema().deserialize(data)
        assert des == data

    def test_url_required(self):
        data = dict(duration=1, visited_at=1)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_duration_required(self):
        data = dict(url='foo', visited_at=1)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_visited_at_required(self):
        data = dict(url='foo', duration=1)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_no_additional_allowed(self):
        data = dict(url='foo', duration=1, visited_at=1, foo='bar')
        des = VisitSchema().deserialize(data)
        assert 'foo' not in des
