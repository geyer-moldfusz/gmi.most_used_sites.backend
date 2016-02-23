from cornice import Service
from colander import Invalid
from pyramid.httpexceptions import HTTPServiceUnavailable
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import json

from .models import DBSession, Visit, User, State
from .responses import VisitsResponse
from .schemas import VisitsSchema, UserSchema


def valid_user(request):
    try:
        request.unique_user_id = UserSchema().deserialize(
            request.matchdict['user'])
    except Invalid:
        request.errors.add('querystring', 'user id', 'invalid id format')

def since(request):
    try:
      request.since = int(request.matchdict['since'][0])
    except KeyError:
      request.since = 0
    except IndexError:
      request.since = 0


all_visits = Service(name='all_visits', path='/visits') # XXX merge into visits service
visits = Service(name='visits', path='/visits/{user}*since', validators=[valid_user, since])
stats = Service(name='stats', path='/stats')


@view_config(route_name='home')
def index(request):
    return Response('<h1>Hello World!</h1>')


@stats.get()
def state_get(request):
    try:
        state = DBSession.query(State).one()
        assert state.intact
    except:
        raise HTTPServiceUnavailable()

    return dict(state='ok')


@all_visits.get()
def all_visits_get(request):
    query = DBSession.query(Visit).order_by(
            Visit.visited_at.desc()).limit(20000)
    return VisitsResponse(query)


@visits.get()
def visits_get(request):
    query = DBSession.query(Visit).join(User).filter(
            User.unique_id==request.unique_user_id,
            Visit.visited_at>request.since
        ).order_by(Visit.visited_at.desc()).limit(20000)
    return VisitsResponse(query)


@visits.post(schema=VisitsSchema)
def visits_post(request):
    try:
        user = DBSession.query(User).filter(
            User.unique_id==request.unique_user_id).one()
    except NoResultFound:
        user = User(unique_id=request.unique_user_id)
        DBSession.add(user)

    for visit_params in request.json_body.get('visits'):
        visit = Visit(**visit_params)
        visit.user = user
        DBSession.add(visit)

    DBSession.flush()   # XXX flush in loop, report failed visits seperately
    return dict()


@visits.post(context=IntegrityError)
def _visit_integrity_error(request):
    response =  Response(json.dumps({'warning': 'visit already submitted'}))
    response.status_int = 205
    response.content_type = 'application/json'
    return response
