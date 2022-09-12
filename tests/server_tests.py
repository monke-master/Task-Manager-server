from unittest import *
from main import Application
from database import Database
from mysql.connector import connect


class TestApplication(TestCase):
    application = None
    flask_app = None

    @classmethod
    def setUpClass(self) -> None:
        # Инициализация тестовой бд
        connection = connect(
            host='localhost',
            user='root',
            password='admin',
            database='testing'
        )
        database = Database()
        database.initialize(connection)
        # Добавление тестовых пользователей
        database.add_user(id=0,
                          email='delete.me@gmail.com',
                          password='password',
                          registration_date='2022-08-11 13:04:00')
        database.add_user(id=1,
                          email='get.me@gmail.com',
                          password='password',
                          registration_date='2022-08-11 13:04:00')
        database.add_user(id=2,
                          email='update.my.email@gmail.com',
                          password='password',
                          registration_date='2022-08-11 13:04:00')
        database.add_user(id=3,
                          email='update.my.passsword@gmail.com',
                          password='password',
                          registration_date='2022-08-11 13:04:00')

        # Добавление тестовых категорий
        database.add_category(category_id=0,
                              user_id=2,
                              title='delete me',
                              creation_date='2022-09-11 11:39:00')
        database.add_category(category_id=1,
                              user_id=1,
                              title='get me',
                              creation_date='2022-09-11 11:39:00')
        database.add_category(category_id=2,
                              user_id=1,
                              title='just category',
                              creation_date='2022-09-11 11:39:00')
        database.add_category(category_id=3,
                              user_id=2,
                              title='update my title',
                              creation_date='2022-09-11 11:39:00')

        # Добавление тестовых задач
        database.add_task(task_id=0,
                          category_id=None,
                          user_id=3,
                          title='Delete me',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=1)
        database.add_task(task_id=1,
                          category_id=2,
                          user_id=1,
                          title='Get this task',
                          date='2022-09-11 22:30:00',
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=2,
                          category_id=2,
                          user_id=1,
                          title='get this task in list',
                          date='2022-09-11 22:30:00',
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=3,
                          category_id=None,
                          user_id=1,
                          title='Just task',
                          date='2022-09-11 22:30:00',
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=4,
                          category_id=None,
                          user_id=2,
                          title='Update title',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=5,
                          category_id=None,
                          user_id=2,
                          title='Update category',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=6,
                          category_id=None,
                          user_id=2,
                          title='Update date',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=7,
                          category_id=None,
                          user_id=2,
                          title='Update emailed',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=8,
                          category_id=None,
                          user_id=2,
                          title='Update completed',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)
        database.add_task(task_id=9,
                          category_id=None,
                          user_id=2,
                          title='Update repeating',
                          date=None,
                          creation_date='2022-09-11 11:39:00',
                          emailed=None,
                          repeating=None,
                          completed=0)

        self.application = Application(database)
        self.application.initialize()
        self.application.app.config['TESTING'] = True
        self.flask_app = self.application.app.test_client()

    # User tests
    def test_get_user(self):
        result = self.flask_app.get('/user/1').get_json()
        expected = {'id': '1',
                    'email': 'get.me@gmail.com',
                    'password': 'password',
                    'registration_date': '2022-08-11 13:04:00'}
        self.assertEqual(result, expected)

    def test_get_user_by_email(self):
        result = self.flask_app.get('/user/email/get.me@gmail.com').get_json()
        expected = {'id': '1',
                    'email': 'get.me@gmail.com',
                    'password': 'password',
                    'registration_date': '2022-08-11 13:04:00'}
        self.assertEqual(expected, result)

    def test_get_non_existing_user(self):
        result = self.flask_app.get('/user/100')
        self.assertEqual(result.status_code, 404)

    def test_get_non_existing_user_by_email(self):
        result = self.flask_app.get('/user/email/non.existing@gmail.com')
        self.assertEqual(result.status_code, 404)

    def test_add_user(self):
        result = self.flask_app.post('/user/20', data={
            "email": 'add.testing@gmail.com',
            'password': 'password',
            'registration_date': '2022-08-11 13:04:00'
        })
        self.assertEqual(result.status_code, 200)

    def test_delete_user(self):
        result = self.flask_app.delete('user/0')
        self.assertEqual(result.status_code, 200)

    def test_update_user_email(self):
        result = self.flask_app.put('user/2', data={
            "email": 'new_email@gmail.com',
            'password': 'password',
        })
        self.assertEqual(result.status_code, 200)

    def test_update_user_password(self):
        result = self.flask_app.put('user/2', data={
            "email": 'update.my.passsword@gmail.com',
            'password': 'new_password',
        })
        self.assertEqual(result.status_code, 200)

    # Categories tests
    def test_get_category(self):
        result = self.flask_app.get("/category/1").get_json()
        expected = {
            'category_id': '1',
            'user_id': '1',
            'title': 'get me',
            'creation_date': '2022-09-11 11:39:00'
        }
        self.assertEqual(expected, result)

    def get_non_existing_category(self):
        result = self.flask_app.get("/category/228")
        self.assertEqual(result.status_code, 404)

    def test_get_categories_list(self):
        result = self.flask_app.get("user/1/categories").get_json()
        expected = {
            '1': {
             'user_id': '1',
             'title': 'get me',
             'creation_date': '2022-09-11 11:39:00'
            },
            '2': {
             'user_id': '1',
             'title': 'just category',
             'creation_date': '2022-09-11 11:39:00'
            }
        }
        self.assertEqual(expected, result)

    def test_get_non_existing_categories_list(self):
        result = self.flask_app.get('/category/list/228')
        self.assertEqual(result.status_code, 404)

    def test_get_non_existing_category(self):
        result = self.flask_app.get("/category/100")
        self.assertEqual(result.status_code, 404)

    def test_add_category(self):
        result = self.flask_app.post("/category/20", data={
            'user_id': '2',
            'title': 'new category',
            'creation_date': '2022-09-11 11:39:00'
        })
        self.assertEqual(result.status_code, 200)

    def test_delete_category(self):
        result = self.flask_app.delete("/category/0")
        self.assertEqual(result.status_code, 200)

    def test_update_category_title(self):
        result = self.flask_app.put("/category/3", data={'title': 'new title'})
        self.assertEqual(result.status_code, 200)

    # Tasks tests
    def test_get_task(self):
        result = self.flask_app.get('/task/1').get_json()
        expected = {
            'task_id': '1',
            'user_id': '1',
            'category_id': '2',
            'title': 'Get this task',
            'date': '2022-09-11 22:30:00',
            'creation_date': '2022-09-11 11:39:00',
            'repeating': None,
            'completed': 0,
            'emailed': None
        }
        self.assertEqual(result, expected)

    def test_get_non_existing_task(self):
        result = self.flask_app.get('/task/228')
        self.assertEqual(result.status_code, 404)

    def test_get_category_tasks(self):
        result = self.flask_app.get('/category/2/tasks').get_json()
        expected = {
            '1': {
                'user_id': '1',
                'category_id': '2',
                'title': 'Get this task',
                'date': '2022-09-11 22:30:00',
                'creation_date': '2022-09-11 11:39:00',
                'repeating': None,
                'completed': 0,
                'emailed': None
            },
            '2': {
                'user_id': '1',
                'category_id': '2',
                'title': 'get this task in list',
                'date': '2022-09-11 22:30:00',
                'creation_date': '2022-09-11 11:39:00',
                'repeating': None,
                'completed': 0,
                'emailed': None
            },
        }
        self.assertEqual(result, expected)

    def test_get_non_existing_category_tasks(self):
        result = self.flask_app.get('/category/200/tasks')
        self.assertEqual(result.status_code, 404)

    def test_get_user_tasks(self):
        result = self.flask_app.get('/user/1/tasks').get_json()
        expected = {
            '1': {
                'user_id': '1',
                'category_id': '2',
                'title': 'Get this task',
                'date': '2022-09-11 22:30:00',
                'creation_date': '2022-09-11 11:39:00',
                'repeating': None,
                'completed': 0,
                'emailed': None
            },
            '2': {
                'user_id': '1',
                'category_id': '2',
                'title': 'get this task in list',
                'date': '2022-09-11 22:30:00',
                'creation_date': '2022-09-11 11:39:00',
                'repeating': None,
                'completed': 0,
                'emailed': None
            },
            '3': {
                'user_id': '1',
                'category_id': None,
                'title': 'Just task',
                'date': '2022-09-11 22:30:00',
                'creation_date': '2022-09-11 11:39:00',
                'repeating': None,
                'completed': 0,
                'emailed': None
            },
        }
        self.assertEqual(result, expected)

    def test_get_non_existing_user_tasks(self):
        result = self.flask_app.get('/user/100/tasks')
        self.assertEqual(result.status_code, 404)

    def test_add_minimal_task(self):
        result = self.flask_app.put('/task/20', data={
            'user_id': '3',
            'category_id': None,
            'title': 'Minimal task',
            'creation_date': '2022-09-12 18:32:00',
            'date': None,
            'completed': 0,
            'repeating': None,
            'emailed': None
        })
        self.assertEqual(result.status_code, 200)

    def test_add_full_task(self):
        result = self.flask_app.post('/task/20', data={
            'user_id': '3',
            'category_id': '3',
            'title': 'Full task',
            'creation_date': '2022-09-12 18:32:00',
            'date': '2022-10-12 18:32:00',
            'completed': 0,
            'repeating': 1500,
            'emailed': 1
        })
        self.assertEqual(result.status_code, 200)

    def test_update_task_title(self):
        result = self.flask_app.put('task/4', data={
            'title': 'New title',
            'category_id': None,
            'date': None,
            'emailed': None,
            'repeating': None,
            'completed': 0
        })
        self.assertEqual(result.status_code, 200)

    def test_update_task_category(self):
        result = self.flask_app.put('task/5', data={
            'title': 'Update category',
            'category_id': 3,
            'date': None,
            'emailed': None,
            'repeating': None,
            'completed': 0
        })
        self.assertEqual(result.status_code, 200)

    def test_update_task_date(self):
        result = self.flask_app.put('task/6', data={
            'title': 'Update date',
            'category_id': None,
            'date': '2022-10-12 22:34:34',
            'emailed': None,
            'repeating': None,
            'completed': 0
        })
        self.assertEqual(result.status_code, 200)

    def test_update_task_emailed(self):
        result = self.flask_app.put('task/7', data={
            'title': 'Update emailed',
            'category_id': None,
            'date': None,
            'emailed': 0,
            'repeating': None,
            'completed': 0
        })
        self.assertEqual(result.status_code, 200)

    def test_update_task_completed(self):
        result = self.flask_app.put('task/8', data={
            'title': 'Update completed',
            'category_id': None,
            'date': None,
            'emailed': None,
            'repeating': None,
            'completed': 1
        })
        self.assertEqual(result.status_code, 200)

    def test_update_task_repeating(self):
        result = self.flask_app.put('task/9', data={
            'title': 'Update repeating',
            'category_id': None,
            'date': None,
            'emailed': None,
            'repeating': 1500,
            'completed': 0
        })
        self.assertEqual(result.status_code, 200)

    
    @classmethod
    def tearDownClass(self) -> None:
        self.application.clean_db()

