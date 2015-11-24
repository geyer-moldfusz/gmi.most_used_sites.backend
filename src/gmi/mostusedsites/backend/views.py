from cornice import Service
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from .models import DBSession, Visit, User


all_visits = Service(name='all_visits', path='/visits')
visits = Service(name='visits', path='/visits/{user}')

@view_config(route_name='home')
def indexview(request):
    return Response('<h1>Hello World!</h1>')

@all_visits.get()
def all_visits_get(request):
    visits = list(map(
        lambda x: dict(url=x.url, visited_at=x.visited_at, duration=x.duration),
        DBSession.query(Visit).all()))
    response = dict(_items=visits)
    return response

@visits.get()
def visits_get(request):
    visits = list(map(
        lambda x: dict(url=x.url, visited_at=x.visited_at, duration=x.duration),
        DBSession.query(Visit).join(User).filter(
            User.unique_id==request.matchdict['user']).all()))
    response = dict(_items=visits)
    return response

@visits.post()
def visits_post(request):
    # XXX validation
    try:
        user = DBSession.query(User).filter(
            User.unique_id==request.matchdict['user']).one()
    except NoResultFound:
        user = User(unique_id=request.matchdict['user'])
        DBSession.add(user)

    for visit in request.json_body:
        user.visits.append(Visit(
            url=visit['url'],
            visited_at=visit['visited_at'],
            duration=visit['duration']))
    return dict()
