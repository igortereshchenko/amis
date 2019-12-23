from domain.models import db, Products, Vendors
import plotly
import plotly.graph_objs as go
import json




def product_vendors_population_bar(name):
    data = db.session.query(Vendors.Vendor_name, db.func.countVendors.vendor_id). join(
        Products, Products.product_id == Vendors.product_idFk)
            filter(Products.Product_name == name).group_by(Vendors.Vendor_name).all()
    bar_plot = [
        go.Bar(
                x=[value[0] for value in data],
                y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar_plot, cls=plotly.utils.PlotlyJSONEncoder)
