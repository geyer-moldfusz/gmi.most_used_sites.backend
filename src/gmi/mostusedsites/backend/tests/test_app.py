from gmi.mostusedsites.backend.models import State
from sqlalchemy.exc import IntegrityError
from webtest.app import AppError
import pytest
import json


class TestApp:
    def test_index(self, app):
        res = app.get('/', status=200)
        assert "Hello World" in res.text

    def test_state(self, app, session):
        session.add(State(intact=True))
        session.flush()
        res = app.get('/stats', status=200)
        assert res.content_type == 'application/json'
        assert res.json['state'] == 'ok'

    def test_state_failed(self, app):
        res = app.get('/stats', status=503)
        assert '503 Service Unavailable' in res.text

    def test_get_all_visits(self, app, test_data):
        res = app.get('/visits', status=200)
        assert res.content_type == 'application/json'
        assert len(res.json['visits']) is 2

    def test_get_visit(self, app, test_data):
        res = app.get('/visits/ujadkapdydazujuksyairpin', status=200)
        assert res.content_type == 'application/json'
        assert len(res.json['visits']) is 2

    def test_get_visit_since(self, app, test_data):
        res = app.get('/visits/ujadkapdydazujuksyairpin/2', status=200)
        assert res.content_type == 'application/json'
        assert len(res.json['visits']) is 1

    def test_post_visit(self, app, session):
        res = app.post_json(
            '/visits/ujadkapdydazujuksyairpin',
            {'visits': [{
                'url': 'http://foo',
                'visited_at': 1,
                'duration': 1,
                'active': True}]},
            status=200)
        session.flush()
        assert res.content_type == 'application/json'
        assert res.json == {}   # XXX

    def test_get_visit_user_invalid(self, app):
        res = app.get('/visits/foo', status=400)
        assert res.content_type == 'application/json'
        assert res.json['errors'][0]['description'] == 'invalid id format'

    def test_post_visit_visit_invalid(self, app, session):
        res = app.post_json(
            '/visits/ujadkapdydazujuksyairpin',
            {'visits': [{'visited_at': 1, 'duration': 1}]},
            status=400)
        assert res.content_type == 'application/json'
        assert res.json['errors'][0]['description'] == 'Required'

    def test_post_visit_user_invalid(self, app, session):
        res = app.post_json(
            '/visits/foo',
            {'visits': [{
                'url': 'http://foo',
                'visited_at': 1,
                'duration': 1,
                'active': True}]},
            status=400)
        assert res.content_type == 'application/json'
        assert res.json['errors'][0]['description'] == 'invalid id format'

    def test_post_visit_existing(self, app, session):
        res = app.post_json(
            '/visits/ujadkapdydazujuksyairpin',
            {'visits': [{
                'url': 'http://test_visit',
                'visited_at': 1,
                'duration': 1,
                'active': True}]},
            status=205)
        assert res.content_type == 'application/json'
        assert res.json['warning'] == 'visit already submitted'
