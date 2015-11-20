from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

from .models import Base
from .settings import Settings


app = Eve(settings=Settings, validator=ValidatorSQL, data=SQL)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()


def factory(global_config, **local_config):
    return app.wsgi_app

def run():
    app.run(debug=True)
