import uuid
from flask import request 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id] 
        except KeyError:
            abort(400, message=f"Store not found") 

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message":"store deleted"}
        except KeyError:
            abort(400,message=f"store not found")   

@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        try:    
            return {"stores": stores}
        except Exception as e:
            abort(400, message=f"Failed to fetch stores")

    @blp.arguments(StoreSchema)
    # @blp.response(200, StoreSchema)
    def post(self, store_data):
        try:

            for store in stores:
                if store["name"] == store_data["name"]:
                    abort(400,message=f"Store already exists")

            store_id = uuid.uuid4().hex
            store = {**store_data, "store_id": store_id}
            stores[store_id] = store_data
            return store, 201
        
        except Exception as e:
            abort(400,message=f"""Failed to create a new store
                                  Error : {e}""")