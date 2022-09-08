from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from database import Database



# Класс серверного приложения
class Application:

    database = None
    app = None
    api = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Application, cls).__new__(cls)
        return cls.instance

    def initialize(self):




        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Task, '/task')
        api.add_resource(User, '/user/<int:user_id>')

        self.app = app
        self.api = api

    def run(self):
        self.app.run(host='localhost', port=8080)

    def clean_db(self):
        self.database.clean_tables()


app = Application()
# Необходимые аргументы в запросах

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('email', type=str)
user_post_parser.add_argument('password', type=str)
user_post_parser.add_argument('registration_date', type=str)

task_post_parser = reqparse.RequestParser()
task_post_parser.add_argument("title", type=str)
task_post_parser.add_argument("completed", type=str)


# Классы ресурсов
class User(Resource):

    def get(self, user_id):
        result = app.database.get_user(user_id)
        if result[1] == 200:
            return result
        elif result == 404:
            abort(404, message='Could not find user')
        else:
            abort(500, message='Internal Server Error')

    def put(self, user_id):
        args = user_post_parser.parse_args()
        result = app.database.add_user(id=user_id,
                                       email=args['email'],
                                       password=args['password'],
                                       registration_date=args['registration_date'])
        return result


class Task(Resource):
    def get(self):
        pass


# Точка входа в программу
if __name__ == "__main__":
    app.initialize()
    app.run()


