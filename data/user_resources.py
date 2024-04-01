from flask_restful import Resource, abort
from data.users import User
from data import db_session
from flask import jsonify
from data.user_parser import parser


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(User).get(news_id)
    if not news:
        abort(404, message=f"User {news_id} not found")


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()

        return jsonify({'users': [
            i.to_dict(only=('name', 'surname', 'age', 'position', 'speciality', 'hashed_password')) for i in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'], )
        session.add(user)
        session.commit()


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {'user': user.to_dict(only=('name', 'surname', 'age', 'position', 'speciality', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id)
        session.delete(user)
        session.commit()
