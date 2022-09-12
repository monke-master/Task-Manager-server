from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from database import Database
from mysql.connector import connect


# Класс серверного приложения
class Application:

    database = None
    app = None
    api = None

    def __init__(self, database):
        self.database = database

    def initialize(self):
        app = Flask(__name__)
        api = Api(app)

        api.add_resource(User, '/user/<string:user_id>')
        api.add_resource(CategoriesList, '/user/<string:user_id>/categories')
        api.add_resource(UsersTasks, '/user/<string:user_id>/tasks')
        api.add_resource(UserEmail, '/user/email/<string:email>')
        api.add_resource(Category, '/category/<string:category_id>')
        api.add_resource(CategoryTasks, '/category/<string:category_id>/tasks')
        api.add_resource(Task, '/task/<string:task_id>')

        self.app = app
        self.api = api

    def run(self):
        self.app.run(host='localhost', port=8080)

    def clean_db(self):
        self.database.clean_tables()


# Инициализация базы данных
connection = connect(
        host='localhost',
        user='root',
        password='admin',
        database='testing'
    )
database = Database()
database.initialize(connection)

# Инициализация сервера
app = Application(database)

# Необходимые аргументы в запросах
user_data_parser = reqparse.RequestParser()
user_data_parser.add_argument('email', type=str)
user_data_parser.add_argument('password', type=str)
user_data_parser.add_argument('registration_date', type=str)

category_data_parser = reqparse.RequestParser()
category_data_parser.add_argument('user_id', type=str)
category_data_parser.add_argument('title', type=str)
category_data_parser.add_argument('creation_date', type=str)

task_data_parser = reqparse.RequestParser()
task_data_parser.add_argument("title", type=str)
task_data_parser.add_argument("completed", type=int)
task_data_parser.add_argument('user_id', type=str)
task_data_parser.add_argument('category_id', type=str)
task_data_parser.add_argument('date', type=str)
task_data_parser.add_argument('creation_date', type=str)
task_data_parser.add_argument('emailed', type=int)
task_data_parser.add_argument('repeating', type=int)


# Классы ресурсов
class User(Resource):

    def get(self, user_id):
        result = app.database.get_user(user_id)
        if result != [] and result is not Exception:
            result_json = {
                'id': result[0][0],
                'email': result[0][1],
                'password': result[0][2],
                'registration_date': result[0][3]}
            return result_json, 200
        elif result == []:
            abort(404, message='User not found')
        else:
            abort(500, message='Internal server error')

    def post(self, user_id):
        args = user_data_parser.parse_args()
        result = app.database.add_user(id=user_id,
                                       email=args['email'],
                                       password=args['password'],
                                       registration_date=args['registration_date'])
        return result

    def delete(self, user_id):
        result = app.database.delete_user(user_id)
        return result

    def put(self, user_id):
        args = user_data_parser.parse_args()
        result = app.database.update_user(user_id=user_id,
                                          email=args['email'],
                                          password=args['password'])
        return result


class UserEmail(Resource):

    def get(self, email):
        result = app.database.get_user_by_email(email)
        if result != [] and result is not Exception:
            result_json = {
                'id': result[0][0],
                'email': result[0][1],
                'password': result[0][2],
                'registration_date': result[0][3]}
            return result_json, 200
        elif result == []:
            abort(404, message='User not found')
        else:
            abort(500, message='Internal server error')


class Category(Resource):

    def get(self, category_id):
        result = app.database.get_category(category_id=category_id)
        if result != [] and result is not Exception:
            result_json = {
                'category_id': result[0][0],
                'user_id': result[0][1],
                'title': result[0][2],
                'creation_date': result[0][3]}
            return result_json, 200
        elif result == []:
            abort(404, message='Category not found')
        else:
            abort(500, message='Internal server error')

    def post(self, category_id):
        args = category_data_parser.parse_args()
        result = app.database.add_category(
            category_id=category_id,
            user_id=args['user_id'],
            title=args['title'],
            creation_date=args['creation_date'])
        return result

    def delete(self, category_id):
        result = app.database.delete_category(category_id)
        return result

    def put(self, category_id):
        args = category_data_parser.parse_args()
        result = app.database.update_category(category_id=category_id,
                                              title=args['title'])
        return result


class CategoriesList(Resource):

    def get(self, user_id):
        result = app.database.get_categories_list(user_id=user_id)
        result_json = {}
        if result != [] and result is not Exception:
            for category in result:
                result_json[category[0]] = {
                    'user_id': category[1],
                    'title': category[2],
                    'creation_date': category[3]}
            return result_json, 200
        elif result == []:
            abort(404, message='Categories not found')
        else:
            abort(500, message='Internal server error')


class Task(Resource):

    def get(self, task_id):
        result = app.database.get_task(task_id=task_id)
        if result != [] and result is not Exception:
            result_json = {
                'task_id': result[0][0],
                'user_id': result[0][1],
                'title': result[0][2],
                'category_id': result[0][3],
                'creation_date': result[0][4],
                'date': result[0][5],
                'completed': result[0][6],
                'emailed': result[0][7],
                'repeating': result[0][8]}
            return result_json, 200
        elif result == []:
            abort(404, message='Task not found')
        else:
            abort(500, message='Internal server error')

    def post(self, task_id):
        args = task_data_parser.parse_args()
        result = app.database.add_task(
            task_id=task_id,
            title=args['title'],
            category_id=args['category_id'],
            user_id=args['user_id'],
            completed=args['completed'],
            date=args['date'],
            creation_date=args['creation_date'],
            emailed=args['emailed'],
            repeating=args['repeating'])
        return result

    def delete(self, task_id):
        result = app.database.delete_task(task_id)
        return result

    def put(self, task_id):
        args = task_data_parser.parse_args()
        result = app.database.update_task(
            task_id=task_id,
            title=args['title'],
            category_id=args['category_id'],
            completed=args['completed'],
            date=args['date'],
            emailed=args['emailed'],
            repeating=args['repeating'])
        return result


class UsersTasks(Resource):

    def get(self, user_id):
        result = app.database.get_users_tasks(user_id=user_id)
        result_json = {}
        if result != [] and result is not Exception:
            for task in result:
                result_json[task[0]] = {
                    'user_id': task[1],
                    'title': task[2],
                    'category_id': task[3],
                    'creation_date': task[4],
                    'date': task[5],
                    'completed': task[6],
                    'emailed': task[7],
                    'repeating': task[8]
                }
            return result_json, 200
        elif result == []:
            abort(404, message='User not found')
        else:
            abort(500, message='Internal server error')


class CategoryTasks(Resource):

    def get(self, category_id):
        result = app.database.get_category_tasks(category_id=category_id)
        result_json = {}
        if result != [] and result is not Exception:
            for task in result:
                result_json[task[0]] = {
                    'user_id': task[1],
                    'title': task[2],
                    'category_id': task[3],
                    'creation_date': task[4],
                    'date': task[5],
                    'completed': task[6],
                    'emailed': task[7],
                    'repeating': task[8]
                }
            return result_json, 200
        elif result == []:
            abort(404, message='Category not found')
        else:
            abort(500, message='Internal server error')


# Точка входа в программу
if __name__ == "__main__":
    app.initialize()
    app.run()


