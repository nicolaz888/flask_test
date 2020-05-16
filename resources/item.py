from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item must have a store associated"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
            return item.json(), 201
        except Exception as ex:
            return {"message": f"An error occurred inserting the item. {ex}"}

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}, 200
        else:
            return {'message': 'Item was not found'}, 400

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    TABLE_NAME = 'items'

    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
