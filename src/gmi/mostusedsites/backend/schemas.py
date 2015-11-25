import colander


class VisitSchema(colander.MappingSchema):
    url = colander.SchemaNode(colander.String())
    duration = colander.SchemaNode(colander.Int())
    visited_at = colander.SchemaNode(colander.Int())

class VisitsSchema(colander.SequenceSchema):
    visit = VisitSchema()
