import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from db import stores, items

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, "item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted"}
        except KeyError:
            abort(400,message=f"item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, request_data, item_id):

        try:
            # print(items)
            item = items[item_id]
            item |= request_data
            return item
        except KeyError:
            abort(404, message=f"item not found")

@blp.route("/item")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return items.values()
        except Exception:
            abort(400, message=f"No items in stores")

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, items_data):

        if items_data["store_id"] not in stores:
            abort(404 ,"Store not found.")
        item_id = uuid.uuid4().hex
        item = {**items_data, "item_id":item_id}
        items[item_id] = item
        return item, 201

    
