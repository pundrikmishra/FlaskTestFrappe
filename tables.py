from flask_table import Table, Col


class Results(Table):
    id = Col('_id', show=False)
    ProductName = Col('ProductName')
    FromLocation = Col("FromLocation")
    ToLocation = Col("ToLocation")
    qty = Col("qty")
    timestamp = Col("timestamp")

