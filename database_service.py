from database import Database
from mysql.connector import connect


class DatabaseService:

    def __init__(self):
        connection = connect(
            host='localhost',
            user='root',
            password='admin',
            database='testing'
        )
        database = Database()
        database.initialize(connection)
        self.database = database

    def get_user(self, user_id):
        result = self.database.get_user(user_id)
        if result != [] and result is not Exception:
            result_json = {
                'id': result[0][0],
                'email': result[0][1],
                'password': result[0][2],
                'registration_date': result[0][3]
            }
            return result_json, 200
        elif result is Exception:
            return result
        return 404



