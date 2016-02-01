from cornice import Service
from colander import Invalid
from pyramid.httpexceptions import HTTPServiceUnavailable
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from .models import DBSession, Visit, User, State
from .schemas import VisitsSchema, UserSchema


def valid_user(request):
    try:
        request.unique_user_id = UserSchema().deserialize(
            request.matchdict['user'])
    except Invalid:
        request.errors.add('querystring', 'user id', 'invalid id format')


all_visits = Service(name='all_visits', path='/visits')
visits = Service(name='visits', path='/visits/{user}', validators=[valid_user])
status = Service(name='status', path='/status')


@view_config(route_name='home')
def index(request):
    return Response('<h1>Hello World!</h1>')


@status.get()
def status_get(request):
    try:
        state = DBSession.query(State).one()
        assert state.intact
    except:
        raise HTTPServiceUnavailable()

    return dict(status='ok')


@all_visits.get()
def all_visits_get(request):
    visits = list(map(
        lambda x: dict(
            host=x.host,
            visited_at=x.visited_at,
            duration=x.duration,
            active=x.active),
        DBSession.query(Visit).order_by(
            Visit.visited_at.desc()).limit(20000).all()))
    response = dict(visits=visits)
    return response


@visits.get()
def visits_get(request):
    visits = list(map(
        lambda x: dict(
            host=x.host,
            visited_at=x.visited_at,
            duration=x.duration,
            active=x.active),
        DBSession.query(Visit).join(User).filter(
            User.unique_id==request.unique_user_id).limit(20000).all()))
    response = dict(_items=visits)
    return response


@visits.post(schema=VisitsSchema)
def visits_post(request):
    try:
        user = DBSession.query(User).filter(
            User.unique_id==request.unique_user_id).one()
    except NoResultFound:
        user = User(unique_id=request.unique_user_id)
        DBSession.add(user)

    for visit in request.json_body.get('visits'):
        user.visits.append(Visit(**visit))
    return dict()
