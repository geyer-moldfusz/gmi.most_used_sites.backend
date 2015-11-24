from pyramid.testing import DummyRequest
from gmi.mostusedsites.backend import views
from gmi.mostusedsites.backend.models import User
import pytest


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
        req = DummyRequest(matchdict=dict(user='ujadkapdydazujuksyairpin'))
        res = views.visits_get(req)
        for visit in res['_items']:
            assert set(visit.keys()) == set(['visited_at', 'duration', 'url'])

    def test_get_visit_existent(self, visits):
        req = DummyRequest(matchdict=dict(user='ujadkapdydazujuksyairpin'))
        res = views.visits_get(req)
        assert res['_items'] == [{
            'duration': 1, 'url': 'test_visit', 'visited_at': 1}]

    def test_get_visit_non_existent(self, visits):
        req = DummyRequest(matchdict=dict(user='foo'))
        res = views.visits_get(req)
        assert res['_items'] == []

    def test_post_visits(self, visits):
        req = DummyRequest(
            matchdict=dict(user='ujadkapdydazujuksyairpin'),
            json_body=[{'url': 'foo', 'visited_at': 1, 'duration': 1}],
            post=True,
            content_type='application/json')
        res = views.visits_post(req)
        assert res != None # XXX

    def test_post_visits_creates_user(self, session, visits):
        req = DummyRequest(
            matchdict=dict(user='blovJoufEo'),
            json_body=[{'url': 'foo', 'visited_at': 1, 'duration': 1}],
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
        res = app.get('/visits/foo')
        assert res.status_code == 200
        assert res.content_type == 'application/json'

    def test_post_visit(self, app, visits):
        res = app.post_json(
            '/visits/ujadkapdydazujuksyairpin',
            [{'url': 'foo', 'visited_at': 1, 'duration': 1}])
        assert res.status_code == 200
        assert res.content_type == 'application/json'
