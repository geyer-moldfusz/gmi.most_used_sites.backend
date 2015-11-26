from cornice.schemas import CorniceSchema
import colander
import string


class UserSchema(colander.SchemaNode):
    schema_type = colander.String
    validator = colander.All(
        colander.Length(min=24, max=24),
        colander.ContainsOnly(string.ascii_letters + string.digits))


class VisitSchema(colander.MappingSchema):
    url = colander.SchemaNode(colander.String())
    duration = colander.SchemaNode(colander.Int())
    visited_at = colander.SchemaNode(colander.Int())


class VisitsSchema(colander.SequenceSchema):
    visit = VisitSchema()


class VisitsPostSchema(colander.MappingSchema):
    visits = VisitsSchema(location='body')
