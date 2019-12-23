from domain.models import db, Vendors, Clothes
import plotly
import plotly.graph_objs as go
import json

def visualization_data():
    data = db.session.query(Vendors.balance,
                            db.func.count(Clothes.clothe_id).label("ClothesQuantity")
                            ).join(Clothes, Vendors.clothe_idIdFk == Clothes.clothe_id).group_by(Vendors.balance).all()
    close_idd=[1,2,3,4,5]
    bar = [
        go.Bar(
            x=[value[0] for value in data],
            y=close_idd
        )
    ]

    return json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)