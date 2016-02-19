from gmi.mostusedsites.backend.responses import VisitsResponse
from gmi.mostusedsites.backend.models import Visit
from pyramid.response import Response

import json
import pytest


@pytest.fixture
def query(session):
    return session.query(Visit)


@pytest.fixture
def visit_response(query):
    return VisitsResponse(query)


@pytest.fixture
def json_response(visit_response, visits):
    return visit_response.text


class TestResponse:

    def test_is_response(self, visit_response):
        assert isinstance(visit_response, Response)

    def test_content_type_is_json(self, visit_response):
        assert visit_response.content_type == 'application/json'

    def test_response_is_valid_json(self, json_response):
        assert json.loads(json_response)

    def test_return_visits(self, json_response):
        assert 'visits' in json.loads(json_response)

    def test_include_visits(self, json_response):
        assert json.loads(json_response)['visits'] == [
            {
                'active': True,
                'duration': 1,
                'host': 'test_visit',
                'visited_at': 1
            }, {
                'active': False,
                'duration': 1,
                'host': 'test_visit',
                'visited_at': 3
            }]
