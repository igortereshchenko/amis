from domain.models import db, Schemas, Entities, Attributes
import plotly
import plotly.graph_objs as go
import json


def schema_distribution_pie(uuid):
    schema = db.session.query(Entities.Id.label("EntityId"),
                              Entities.Name.label("EntityName"),
                              db.func.count(Attributes.Id).label("AttributesQuantity")).join(
        Schemas, Entities.SchemaIdFk == Schemas.Id).join(
        Attributes, Attributes.EntityIdFk == Entities.Id).filter(Schemas.Id == uuid).group_by(
        Schemas.Id, Entities.Id).subquery()

    data = db.session.query(schema.c.EntityName, db.func.sum(schema.c.AttributesQuantity)
                            ).group_by(schema.c.EntityId, schema.c.EntityName).all()

    pie_plot = [
        go.Pie(
            labels=[value[0] for value in data],
            values=[value[1] for value in data]
        )
    ]

    return json.dumps(pie_plot, cls=plotly.utils.PlotlyJSONEncoder)


def entity_attributes_population_bar(name):
    data = db.session.query(Attributes.Name, db.func.count(Attributes.Id)).join(
        Entities, Entities.Id == Attributes.EntityIdFk
    ).filter(Entities.Name == name).group_by(Attributes.Name).all()

    bar_plot = [
        go.Bar(
            x=[value[0] for value in data],
            y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar_plot, cls=plotly.utils.PlotlyJSONEncoder)
