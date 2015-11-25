from gmi.mostusedsites.backend.schemas import VisitsSchema, VisitSchema
import colander
import pytest


class TestVisitsSchema:
    def test_visits_schema(self):
        data = [dict(url='foo', duration=1, visited_at=1)]
        des = VisitsSchema().deserialize(data)
        assert des == data


class TestVisitSchema:
    def test_schema(self):
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
