from domain.models import db, Schemas, Entities, Attributes
import plotly
import numpy as np
import plotly.graph_objs as go
import json
from .classification import EntityNameClassification


def classification(attributes):
    return EntityNameClassification().execute(attributes)


def correlation():
    schemas = db.session.query(Schemas.Id.label("SchemaId"),
                               Entities.Id.label("EntityId"),
                               db.func.count(Attributes.Id).label("AttributesQuantity")).join(
        Schemas, Entities.SchemaIdFk == Schemas.Id).join(
        Attributes, Attributes.EntityIdFk == Entities.Id).group_by(
        Schemas.Id, Entities.Id).subquery()

    data = db.session.query(db.func.count(schemas.c.EntityId), db.func.sum(schemas.c.AttributesQuantity)
                            ).group_by(schemas.c.SchemaId).all()

    scatter = go.Figure(data=go.Scatter(x=[value[0] for value in data],
                                        y=[value[1] for value in data],
                                        mode='markers',
                                        marker=dict(
                                            size=16,
                                            color=np.random.randn(500),
                                            colorscale='Viridis'
                                        )))

    return json.dumps(scatter, cls=plotly.utils.PlotlyJSONEncoder)
