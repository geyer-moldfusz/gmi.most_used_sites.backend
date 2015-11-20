from eve.utils import config
from eve_sqlalchemy.decorators import registerSchema
from .models import User, Site


ID_FIELD = 'id'
ITEM_LOOKUP_FIELD = ID_FIELD
config.ID_FIELD = ID_FIELD
config.ITEM_LOOKUP_FIELD = ID_FIELD

registerSchema('user')(User)
registerSchema('site')(Site)


Settings = {
    'ID_FIELD': 'id',
    'ITEM_LOOKUP_FIELD': 'id',
    'INFO': '_info',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/test.db',
    'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
    'DOMAIN': {
      'user': User._eve_schema['user'],
      'sites': Site._eve_schema['site']
    }
}
