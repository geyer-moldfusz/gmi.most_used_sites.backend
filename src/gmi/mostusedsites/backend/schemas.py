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
    active = colander.SchemaNode(colander.Boolean())


class VisitListSchema(colander.SequenceSchema):
    visit = VisitSchema()


class VisitsSchema(colander.MappingSchema):
    visits = VisitListSchema(location='body')
