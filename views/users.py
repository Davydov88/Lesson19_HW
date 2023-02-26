from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from utils import auth_required, admin_required


user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200


    def post(self):
        data = request.json
        user = user_service.create(data)
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        user = user_service.get_one(uid)
        user_data = UserSchema().dump(user)
        return user_data, 200

    @admin_required
    def put(self, uid):
        data = request.json
        if 'id' not in data:
            data['id'] = uid
        user_service.update(data)
        return "", 204

    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204





