from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import StoreModel


blp = Blueprint('stores', __name__, description='Operations on store')


@blp.route('/stores/<int:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        item = StoreModel.query.get_or_404(store_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Store deleted'}


@blp.route('/stores')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='Error with adding the new store.')

        return store
