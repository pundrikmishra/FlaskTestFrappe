from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
import datetime
# from flask_table import Table, Col
from tables import Results


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/frappeTest"
mongo = PyMongo(app)
api = Api(app)

############################### Product #########################################


class AddProduct(Resource):
    def post(self):
        product = mongo.db.product
        ProductName = request.json['ProductName']
        if product.find_one({"ProductName": ProductName}):
            return jsonify({"Message": "Product Already Existed"})
        else:
            NewProductId = product.insert({"ProductName": ProductName})
            NewProduct = product.find_one({"_id": NewProductId})
            output = {"ProductName": NewProduct['ProductName']}
            return jsonify({"New Product Added": output})

        # product = mongo.db.product
        # location = mongo.db.location
        # ProductName = request.json['ProductName']
        # qty = request.json['qty']
        # # qty = int(qty)
        # LocationName = request.json['LocationName']
        # if location.find_one({"LocationName": LocationName}):
        #     if product.find_one({"ProductName": ProductName, "LocationName": LocationName}):
        #             return jsonify({"Message": "Product Already Existed"})
        #     else:
        #         NewProductId = product.insert({"ProductName": ProductName, "qty": qty, "LocationName": LocationName})
        #         NewProduct = product.find_one({"_id": NewProductId})
        #         output = {"ProductName": NewProduct['ProductName'], "qty": NewProduct['qty'],
        #                   "LocationName": NewProduct['LocationName']}
        #         return jsonify({"New Product Added": output})
        # else:
        #     return jsonify({"Message": "Location Not Existed"})


class ViewProduct(Resource):
    def get(self):
        product = mongo.db.product
        output = []
        for all_product in product.find():
            output.append({'ProductName': all_product['ProductName']})
        return jsonify({'All Product': output})

        # product = mongo.db.product
        # output = []
        # for all_product in product.find():
        #     output.append({'ProductName': all_product['ProductName'], "qty": all_product['qty'],
        #                    "LocationName": all_product['LocationName']})
        # return jsonify({'All Product': output})


class EditProduct(Resource):
    def post(self):
        product = mongo.db.product
        OldProductName = request.json['OldProductName']
        NewProductName = request.json['NewProductName']
        if product.find_one({"ProductName": OldProductName}):
            EditProductId = product.update({"ProductName": OldProductName}, {"$set": {"ProductName": NewProductName}})
            if EditProductId:
                return jsonify({"Message": "Product updated"})
            else:
                return jsonify({"Message": "Product Not Updated"})
        else:
            return jsonify({"Message": "Product is Not in Database"})

        # product = mongo.db.product
        # ProductName = request.json['ProductName']
        # LocationName = request.json['LocationName']
        # # OldQty = request.json['OldQty']
        # NewQty = request.json['NewQty']
        # if product.find_one({"ProductName": ProductName, "LocationName": LocationName}):
        #     EditProductQtyId = product.update({"ProductName": ProductName, "LocationName": LocationName},
        #                                       {"$set": {"qty": NewQty}})
        #     # NewProduct = product.find_one({"_id": EditProductQtyId})
        #     if EditProductQtyId:
        #         return jsonify({"Message": "Product Qty updated"})
        #     else:
        #         return jsonify({"Message": "Product Qty Not Updated"})
        # else:
        #     return jsonify({"Message": "Product is Not at this Location"})


# class DeleteProduct(Resource):
#     def post(self):
#         product = mongo.db.product
#         ProductName = request.json['ProductName']
#         if product.find_one({"ProductName": ProductName}):
#             DeleteProductId = product.delete_one({"ProductName": ProductName})
#             if DeleteProductId:
#                 return jsonify({"Message": "Product Deleted"})
#             else:
#                 return jsonify({"Message": "Product Not Deleted"})
#         else:
#             return jsonify({"Message": "Product is Not in Database"})
############################### Location #########################################


class AddLocation(Resource):
    def post(self):
        location = mongo.db.location
        LocationName = request.json['LocationName']
        if location.find_one({"LocationName": LocationName}):
                return jsonify({"Message": "Location Already Existed"})
        else:
            NewLocationId = location.insert({"LocationName": LocationName})
            NewLocation = location.find_one({"_id": NewLocationId})
            output = {"LocationName": NewLocation['LocationName']}
            return jsonify({"New Location Added": output})


class ViewLocation(Resource):
    def get(self):
        location = mongo.db.location
        output = []
        for all_location in location.find():
            output.append({'LocationName': all_location['LocationName']})
        return jsonify({'All Location': output})


class EditLocation(Resource):
    def post(self):
        location = mongo.db.location
        product = mongo.db.product
        OldLocationName = request.json['OldLocationName']
        NewLocationName = request.json['NewLocationName']
        if location.find_one({"LocationName": OldLocationName}):
            EditLocationId = location.update({"LocationName": OldLocationName},
                                             {"$set": {"LocationName": NewLocationName}})
            # EditProductLocationId = product.find_one({"LocationName": OldLocationName})
            # return jsonify({"Message": EditProductLocationId})
            # for i in EditProductLocationId:
            # #     product.update({"LocationName": OldLocationName}, {"$set": {"LocationName": NewLocationName}})
            if EditLocationId:
                return jsonify({"Message": "Location Updated"})
            else:
                return jsonify({"Message": "Location Not Updated"})
        else:
            return jsonify({"Message": "Old Location is Not in Database"})


# class DeleteLocation(Resource):
#     def post(self):
#         location = mongo.db.location
#         LocationName = request.json['LocationName']
#         if location.find_one({"LocationName": LocationName}):
#             DeleteLocationId = location.delete_one({"LocationName": LocationName})
#             if DeleteLocationId:
#                 return jsonify({"Message": "Location Deleted"})
#             else:
#                 return jsonify({"Message": "Location Not Deleted"})
#         else:
#             return jsonify({"Message": "Location is Not in Database"})

############################### Product Movement #################################


class AddProductMovement(Resource):
    def post(self):
        product = mongo.db.product
        location = mongo.db.location
        productMovement = mongo.db.productMovement
        ProductName = request.json['ProductName']
        FromLocation = request.json['FromLocation']
        ToLocation = request.json['ToLocation']
        qty = request.json['qty']
        qty = int(qty)
        timestamp = str(datetime.datetime.now())
        ProductInDatabase = product.find_one({"ProductName": ProductName})
        LocationInDatabase = location.find_one({"LocationName": FromLocation})
        # if product.find_one({"ProductName": ProductName}) & location.find_one({"LocationName": FromLocation}
        #                                                                       , {"LocationName": ToLocation}):
        if ProductInDatabase and LocationInDatabase:
            if productMovement.find_one({"ProductName": ProductName, "FromLocation": FromLocation}):
                # If product and and location already in same row then update only qty and time
                QtyInDatabase = productMovement.find_one({"ProductName": ProductName, "FromLocation": FromLocation})
                qty = QtyInDatabase['qty'] + qty
                NewProductMovementId = productMovement.update({"ProductName": ProductName,
                                                               "FromLocation": FromLocation},
                                                               # "ToLocation": ToLocation},
                                                              {"$set": {"qty": qty,
                                                               "timestamp": timestamp}})
                # NewProductMovement = productMovement.find_one({"_id": NewProductMovementId})
                # output = {"ProductName": NewProductMovement['ProductName'],
                #           "FromLocation": NewProductMovement['FromLocation'],
                #           # "ToLocation": NewProductMovement['ToLocation'],
                #           "qty": NewProductMovement['qty'],
                #           "timestamp": NewProductMovement['timestamp']}
                if NewProductMovementId:
                    return jsonify({"Message": "ProductMovement Qty Added"})
                else:
                    return jsonify({"Message": "ProductMovement Qty Not Added"})
            else:
                NewProductMovementId = productMovement.insert({"ProductName": ProductName,
                                                               "FromLocation": FromLocation,
                                                               "ToLocation": ToLocation,
                                                               "qty": qty,
                                                               "timestamp": timestamp})
                NewProductMovement = productMovement.find_one({"_id": NewProductMovementId})
                output = {"ProductName": NewProductMovement['ProductName'],
                          "FromLocation": NewProductMovement['FromLocation'],
                          "ToLocation": NewProductMovement['ToLocation'],
                          "qty": NewProductMovement['qty'],
                          "timestamp": NewProductMovement['timestamp']}
                return jsonify({"New ProductMovement Added": output})
        else:
            return jsonify({"Message": "Product or Location is Not in Database"})

@app.route('/view_product_movement')
def ViewProductMovement():
    productMovement = mongo.db.productMovement
    output = []
    for all_product in productMovement.find():
        output.append({"ProductName": all_product['ProductName'],
                       "FromLocation": all_product['FromLocation'],
                       "ToLocation": all_product['ToLocation'],
                       "qty": all_product['qty'],
                       "timestamp": all_product['timestamp']})
    table = Results(output)
    table.border = True
    return render_template('result.html', table=table)

# class ViewProductMovement(Resource, Table):
#     id = Col('_id', show=False)
#     ProductName = Col('ProductName')
#     FromLocation = Col("FromLocation")
#     ToLocation = Col("ToLocation")
#     qty = Col("qty")
#     timestamp = Col("timestamp")
#     def get(self):
#         productMovement = mongo.db.productMovement
#         output = []
#         for all_product in productMovement.find():
#             output.append({"ProductName": all_product['ProductName'],
#                            "FromLocation": all_product['FromLocation'],
#                            "ToLocation": all_product['ToLocation'],
#                            "qty": all_product['qty'],
#                            "timestamp": all_product['timestamp']})
#         table = ViewProductMovement(output)
#         return jsonify(table)
#         # return jsonify({'All Product Movement': output})


class EditProductMovement(Resource):
    def post(self):
        # product = mongo.db.product
        # location = mongo.db.location
        productMovement = mongo.db.productMovement
        ProductName = request.json['ProductName']
        FromLocation = request.json['FromLocation']
        ToLocation = request.json['ToLocation']
        qty = request.json['qty']
        qty = int(qty)
        timestamp = str(datetime.datetime.now())
        # ProductInDatabase = product.find_one({"ProductName": ProductName})
        # LocationInDatabase = location.find_one({"LocationName": FromLocation})
        # ProductLocationQty = productMovement.find({"ProductName": ProductName, "$or":
        #                                            {"FromLocation": FromLocation,
        #                                             "ToLocation": ToLocation }})

        ProductLocationQtyId = productMovement.find_one({"ProductName": ProductName,
                                                   "FromLocation": FromLocation})
        QtyInDatabase = ProductLocationQtyId['qty']
        if productMovement.find_one({"ProductName": ProductName, "FromLocation": FromLocation}):
            if productMovement.find_one({"ProductName": ProductName, "FromLocation": FromLocation, "qty": {"$gt": qty}}):
                updatedQty = QtyInDatabase - qty
                NewProductMovementId = productMovement.update({"ProductName": ProductName,
                                                               "FromLocation": FromLocation},
                                                              {"$set": {"qty": updatedQty,
                                                                        "ToLocation": ToLocation,
                                                                        "timestamp": timestamp}})
                ProductQtyAtLocationId = 0
                ProductAtNewLocationId = 0
                if productMovement.find_one({"ProductName": ProductName, "FromLocation": ToLocation}):
                    ProductLocationQtyId = productMovement.find_one({"ProductName": ProductName,
                                                                     "FromLocation": ToLocation})
                    LocationQtyInDatabase = ProductLocationQtyId['qty']
                    LocationQtyUpdated = LocationQtyInDatabase + qty
                    ProductQtyAtLocationId = productMovement.update({"ProductName": ProductName,
                                                                     "FromLocation": ToLocation},
                                                                    {"$set": {"qty": LocationQtyUpdated,
                                                                              # "ToLocation": ToLocation,
                                                                              "timestamp": timestamp}}
                                                                    )
                else:
                    ProductAtNewLocationId = productMovement.insert({"ProductName": ProductName,
                                                                     "FromLocation": ToLocation,
                                                                     "ToLocation": "",
                                                                     "qty": qty,
                                                                     "timestamp": timestamp})
                if NewProductMovementId and (ProductQtyAtLocationId or ProductAtNewLocationId):
                    return jsonify({"Message": "Product Movement is done"})
                else:
                    return jsonify({"Message": "ProductMovement not done "})
            else:
                return jsonify({"Message": "Only" + QtyInDatabase + "Product quantity is available in database"})
        else:
            return jsonify({"Message": "Product is not available at this location"})


api.add_resource(AddProduct, '/add_product')
api.add_resource(ViewProduct, '/view_product')
api.add_resource(EditProduct, '/edit_product')
# api.add_resource(DeleteProduct, '/delete_product')


api.add_resource(AddLocation, '/add_location')
api.add_resource(ViewLocation, '/view_location')
api.add_resource(EditLocation, '/edit_location')
# api.add_resource(DeleteLocation, '/delete_location')


api.add_resource(AddProductMovement, '/add_product_movement')
# api.add_resource(ViewProductMovement, '/view_product_movement')
api.add_resource(EditProductMovement, '/edit_product_movement')
# api.add_resource(MoveProductMovement, '/move_product_movement')
# api.add_resource(DeleteProductMovement, '/delete_product_movement')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
