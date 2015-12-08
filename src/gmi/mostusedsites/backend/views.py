from cornice import Service
from colander import Invalid
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from .models import DBSession, Visit, User
from .schemas import VisitsSchema, UserSchema


def valid_user(request):
    try:
        request.unique_user_id = UserSchema().deserialize(
            request.matchdict['user'])
    except Invalid:
        request.errors.add('querystring', 'user id', 'invalid id format')


all_visits = Service(name='all_visits', path='/visits')
visits = Service(name='visits', path='/visits/{user}', validators=[valid_user])


@view_config(route_name='home')
def indexview(request):
    return Response('<h1>Hello World!</h1>')


@all_visits.get()
def all_visits_get(request):
    visits = list(map(
        lambda x: dict(
            host=x.host,
            visited_at=x.visited_at,
            duration=x.duration,
            active=x.active),
        DBSession.query(Visit).all()))
    response = dict(_items=visits)
    return response


@visits.get()
def visits_get(request):
    visits = list(map(
        lambda x: dict(
            host=x.host,
            scheme=x.scheme,
            path=x.path,
            visited_at=x.visited_at,
            duration=x.duration,
            active=x.active),
        DBSession.query(Visit).join(User).filter(
            User.unique_id==request.unique_user_id).all()))
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
