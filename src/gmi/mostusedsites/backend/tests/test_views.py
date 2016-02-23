from cornice.errors import Errors
from gmi.mostusedsites.backend import views
from gmi.mostusedsites.backend.models import User, State
from pyramid.httpexceptions import HTTPServiceUnavailable
from pyramid import testing
from sqlalchemy import inspect
import pytest
import json


class TestValidation:
    def test_valid_user(self):
        req = testing.DummyRequest(matchdict=dict(user='fooptipjiWetAdujOgfiflaj'))
        views.valid_user(req)
        assert req.unique_user_id == req.matchdict['user']

    def test_invalid_user(self):
        req = testing.DummyRequest(matchdict=dict(user='foo'))
        setattr(req, 'errors', Errors(req))
        views.valid_user(req)
        assert req.errors == [{
            'name': 'user id',
            'description': 'invalid id format',
            'location': 'querystring'}]

    def test_since(self):
        req = testing.DummyRequest(matchdict=dict(
            user='fooptipjiWetAdujOgfiflaj',
            since=('12345',)))
        views.since(req)
        assert req.since == 12345

    def test_since_undefined(self):
        req = testing.DummyRequest(matchdict=dict(user='fooptipjiWetAdujOgfiflaj'))
        views.since(req)
        assert req.since == 0

    def test_since_not_set(self):
        req = testing.DummyRequest(matchdict=dict(
            user='fooptipjiWetAdujOgfiflaj',
            since=()))
        views.since(req)
        assert req.since == 0


class TestView:
    def test_index(self):
        req = testing.DummyRequest()
        res = views.index(req)
        assert res.status_code == 200

    def test_state(self, session):
        session.add(State(intact=True))
        session.flush()
        req = testing.DummyRequest()
        res = views.state_get(req)
        assert res == {'state': 'ok'}

    def test_state_failure(self, session):
        session.add(State(intact=False))
        session.flush()
        req = testing.DummyRequest()
        with pytest.raises(HTTPServiceUnavailable) as e:
            res = views.state_get(req)
        assert 'The server is currently unavailable' in str(e)

    def test_all_visits(self, session):
        req = testing.DummyRequest()
        res = json.loads(views.all_visits_get(req).text)
        assert res['visits'] != []
        for visit in res['visits']:
            assert set(visit.keys()) == set(
                ['visited_at', 'duration', 'host', 'active'])

    def test_all_visits_does_not_expose_path(self, session):
        req = testing.DummyRequest()
        res = json.loads(views.all_visits_get(req).text)
        for visit in res['visits']:
            assert "foo" not in visit['host']

    def test_all_visits_does_not_expose_params(self, session):
        req = testing.DummyRequest()
        res = json.loads(views.all_visits_get(req).text)
        for visit in res['visits']:
            assert "?" not in visit['host']

    def test_get_visits(self, session):
        req = testing.DummyRequest(
            unique_user_id='ujadkapdydazujuksyairpin', since=0)
        res = json.loads(views.visits_get(req).text)
        for visit in res['visits']:
            assert set(visit.keys()) == set(
                ['visited_at', 'duration', 'host', 'active'])

    def test_get_visits_existent(self, session):
        req = testing.DummyRequest(
            unique_user_id='ujadkapdydazujuksyairpin', since=0)
        res = json.loads(views.visits_get(req).text)
        assert res['visits'] == [
            {
                'duration': 1,
                'host': 'test_visit',
                'visited_at': 3,
                'active': False
            }, {
                'duration': 1,
                'host': 'test_visit',
                'visited_at': 1,
                'active': True
            }]

    def test_get_visits_since(self, session):
        req = testing.DummyRequest(
            unique_user_id='ujadkapdydazujuksyairpin', since=2)
        res = json.loads(views.visits_get(req).text)
        assert res['visits'] == [
            {
                'duration': 1,
                'host': 'test_visit',
                'visited_at': 3,
                'active': False
            }]

    def test_get_visits_non_existent(self, session):
        req = testing.DummyRequest(unique_user_id='foo', since=0)
        res = json.loads(views.visits_get(req).text)
        assert res['visits'] == []

### Path is not delivered any longer ###
#    def test_get_visits_does_not_expose_params(self, session):
#        req = testing.DummyRequest(
#            unique_user_id='ujadkapdydazujuksyairpin', since=0)
#        res = json.loads(views.visits_get(req).text)
#        for visit in res['visits']:
#            assert "?" not in visit['path']

    def test_post_visits(self, session):
        req = testing.DummyRequest(
            unique_user_id='ujadkapdydazujuksyairpin',
            json_body={'visits': [{
                'url': 'http://foo',
                'visited_at': 1,
                'duration': 1,
                'active': True}]},
            post=True,
            content_type='application/json')
        res = views.visits_post(req)
        assert res != None # XXX

    def test_post_visits_creates_user(self, session):
        req = testing.DummyRequest(
            unique_user_id='blovJoufEo',
            json_body={'visits': [{
                'url': 'http://foo',
                'visited_at': 1,
                'duration': 1,
                'active': True}]},
            post=True,
            content_type='application/json')
        res = views.visits_post(req)
        assert session.query(User).filter(User.unique_id=='blovJoufEo').one()

    def test_post_visit_does_not_load_all_visits(self, session):
        user = session.query(User).filter(
            User.unique_id=='ujadkapdydazujuksyairpin').one()
        req = testing.DummyRequest(
            unique_user_id='ujadkapdydazujuksyairpin',
            json_body={'visits': [{
                'url': 'http://foo',
                'visited_at': 1,
                'duration': 1,
                'active': True}]},
            post=True,
            content_type='application/json')
        res = views.visits_post(req)
        ins = inspect(user)
        assert 'visits' in ins.unloaded
