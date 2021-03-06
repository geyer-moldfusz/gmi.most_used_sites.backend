from gmi.mostusedsites.backend.schemas import (
    VisitsSchema,
    VisitListSchema,
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
        data = {
            'visits': [{
                'url': 'http://foo',
                'duration': 1,
                'visited_at': 1,
                'active': True}]}
        des = VisitsSchema().deserialize(data)
        assert des == data

    def test_visits_missing(self):
        data = {'foo': 'bar'}
        with pytest.raises(colander.Invalid):
            des = VisitsSchema().deserialize(data)

    def test_additional_data(self):
        data = {
            'visits': [{
                'url': 'http://foo',
                'duration': 1,
                'visited_at': 1,
                'active': True}],
            'foo': 'bar'}
        des = VisitsSchema().deserialize(data)
        assert 'foo' not in des


class TestVisitListSchema:
    def test_valid(self):
        data = [{
            'url': 'http://foo',
            'duration': 1,
            'visited_at': 1,
            'active': True}]
        des = VisitListSchema().deserialize(data)
        assert des == data

    def test_no_list(self):
        data = {
            'url': 'http://foo',
            'duration': 1,
            'visited_at': 1,
            'active': True}
        with pytest.raises(colander.Invalid):
            VisitListSchema().deserialize(data)


class TestVisitSchema:
    def test_valid(self):
        data = dict(url='http://foo', duration=1, visited_at=1, active=True)
        des = VisitSchema().deserialize(data)
        assert des == data

    def test_url_required(self):
        data = dict(duration=1, visited_at=1, active=True)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_url_invalid_scheme(self):
        data = dict(url='foo', duration=1, visited_at=1, active=True)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_duration_required(self):
        data = dict(url='http://foo', visited_at=1, active=True)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_visited_at_required(self):
        data = dict(url='http://foo', duration=1, active=True)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_active_required(self):
        data = dict(url='http://foo', duration=1, visited_at=1)
        with pytest.raises(colander.Invalid):
            VisitSchema().deserialize(data)

    def test_additional_data(self):
        data = dict(
            url='http://foo', duration=1, visited_at=1, active=True, foo='bar')
        des = VisitSchema().deserialize(data)
        assert 'foo' not in des
