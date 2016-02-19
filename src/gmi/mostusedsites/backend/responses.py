from pyramid.response import Response
import json


class VisitsResponse(Response):
    def __init__(self, query, *args, **kwargs):
        super(VisitsResponse, self).__init__(*args, **kwargs)
        self.content_type = 'application/json'
        self.app_iter = self._generator(query)

    def _generator(self, query):
        first = True

        yield b'{"visits": ['

        for v in query.yield_per(10):
            if first:
                first = False
            else:
                yield b','

            visit = dict(
                host=v.host,
                visited_at=v.visited_at,
                duration=v.duration,
                active=v.active)
            yield str.encode(json.dumps(visit))

        yield b']}'
