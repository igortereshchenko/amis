from domain.models import db, Products, Tests
import plotly
import plotly.graph_objs as go
import json

def visualization_data():
    data = db.session.query(Products.Product_price,
                            db.func.count(Tests.test_id).label("TestsPopulary")
                            ).join(Tests, Products.test_idIdFk == Tests.test_id).group_by(Products.Product_price).all()
    close_idd=[100,200,300,400,500]
    bar = [
        go.Bar(
            x=[value[0] for value in data],
            y=close_idd
        )
    ]

    return json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)