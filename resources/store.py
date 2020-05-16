from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message': 'store was not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'store already exists'}, 400
        store = StoreModel(name)

        try:
            store.save_to_db()
            return store.json(), 201
        except Exception as e:
            return {'message': f'An error ocurred while creating the store {e}'}, 500

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'store deleted'}, 200

        return {'message': 'store does not exist'}, 400


class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
