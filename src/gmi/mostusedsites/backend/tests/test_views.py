from cornice.errors import Errors
from gmi.mostusedsites.backend import views
from gmi.mostusedsites.backend.models import User
from pyramid.testing import DummyRequest
from webtest.app import AppError
import colander
import pytest


class TestValidation:
    def test_valid_user(self):
        req = DummyRequest(matchdict=dict(user='fooptipjiWetAdujOgfiflaj'))
        views.valid_user(req)
        assert req.unique_user_id == req.matchdict['user']

    def test_invalid_user(self):
        req = DummyRequest(matchdict=dict(user='foo'))
        setattr(req, 'errors', Errors(req))
        views.valid_user(req)
        assert req.errors == [{
            'name': 'user id',
            'description': 'invalid id format',
            'location': 'querystring'}]


class TestView:
    def test_index(self):
        req = DummyRequest()
        res = views.indexview(req)
        assert res.status_code == 200

    def test_all_visits(self, visits):
        req = DummyRequest()
        res = views.all_visits_get(req)
        assert res['_items'] != []
        for visit in res['_items']:
            assert set(visit.keys()) == set(['visited_at', 'duration', 'url'])

    def test_get_visit(self, visits):
        req = DummyRequest(unique_user_id='ujadkapdydazujuksyairpin')
        res = views.visits_get(req)
        for visit in res['_items']:
            assert set(visit.keys()) == set(['visited_at', 'duration', 'url'])

    def test_get_visit_existent(self, visits):
        req = DummyRequest(unique_user_id='ujadkapdydazujuksyairpin')
        res = views.visits_get(req)
        assert res['_items'] == [{
            'duration': 1, 'url': 'http://test_visit', 'visited_at': 1}]

    def test_get_visit_non_existent(self, visits):
        req = DummyRequest(unique_user_id='foo')
        res = views.visits_get(req)
        assert res['_items'] == []

    def test_post_visits(self, visits):
        req = DummyRequest(
            unique_user_id='ujadkapdydazujuksyairpin',
            json_body={'visits': [
                {'url': 'http://foo', 'visited_at': 1, 'duration': 1, 'active': True}
            ]},
            post=True,
            content_type='application/json')
        res = views.visits_post(req)
        assert res != None # XXX

    def test_post_visits_creates_user(self, session, visits):
        req = DummyRequest(
            unique_user_id='blovJoufEo',
            json_body={'visits': [
                {'url': 'http://foo', 'visited_at': 1, 'duration': 1, 'active': True}
            ]},
            post=True,
            content_type='application/json')
        res = views.visits_post(req)
        assert session.query(User).filter(User.unique_id=='blovJoufEo').one()


class TestFunctional:
    def test_index(self, app):
        res = app.get('/')
        assert res.status_code == 200

    def test_get_all_visits(self, app, visits):
        res = app.get('/visits')
        assert res.status_code == 200
        assert res.content_type == 'application/json'

    def test_get_visit(self, app, visits):
        res = app.get('/visits/ujadkapdydazujuksyairpin')
        assert res.status_code == 200
        assert res.content_type == 'application/json'

    def test_get_visit_user_invalid(self, app):
        with pytest.raises(AppError) as e:
            res = app.get('/visits/foo')
        assert '400 Bad Request' in str(e)

    def test_post_visit(self, app, visits):
        res = app.post_json(
            '/visits/ujadkapdydazujuksyairpin',
            {'visits': [
                {'url': 'http://foo', 'visited_at': 1, 'duration': 1, 'active': True}
            ]})
        assert res.status_code == 200
        assert res.content_type == 'application/json'

    def test_post_visit_visit_invalid(self, app):
        with pytest.raises(AppError) as e:
            res = app.post_json(
                '/visits/ujadkapdydazujuksyairpin',
                {'visits': [{'visited_at': 1, 'duration': 1}]})
        assert '400 Bad Request' in str(e)

    def test_post_visit_user_invalid(self, app):
        with pytest.raises(AppError) as e:
            res = app.post_json(
                '/visits/foo',
                {'visits': [{
                    'url': 'http://foo',
                    'visited_at': 1,
                    'duration': 1,
                    'active': True}]})
        assert '400 Bad Request' in str(e)
