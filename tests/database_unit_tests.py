import unittest
from database import Database
from mysql.connector import *
from datetime import datetime

class TestDatabase(unittest.TestCase):
    database = None
    cursor = None
    connection = None
    creation_date = str(datetime(2022, 8, 11, 13, 4))
    reg_date = str(datetime(2022, 9, 3, 22, 49))

    @classmethod
    def setUpClass(self) -> None:
        connection = connect(
            host='localhost',
            user='root',
            password='admin',
            database='testing'
        )

        self.cursor = connection.cursor()

        # Добавление тестовых данных
        testing_data = '''INSERT INTO users (id, email, password, registration_date) VALUES (%s, %s, %s, %s)'''
        values = [
            ('10000', 'get_me@gmail.com', 'very_strong_password', self.reg_date),
            ('10001', 'delete_me@gmail.com', 'password', self.reg_date),
            ('10002', 'for.tasks@gmail.com', 'password', self.reg_date),
            ('10003', 'change_my_email@mail.ru', 'password', self.reg_date),
            ('10004', 'change_my_password@mail.ru', 'password', self.reg_date),
            ('10005', 'for_categories@mail.ru', 'password', self.reg_date)
        ]
        self.cursor.executemany(testing_data, values)
        connection.commit()

        testing_categories = '''INSERT INTO categories (category_id, user_id, title, creation_date) VALUES (%s, %s, 
                             %s, %s) '''
        values = [
            ('10000', '10002', 'get this task', self.creation_date),
            ('10001', '10002', 'delete this task', self.creation_date),
            ('10002', '10002', 'update title', self.creation_date),
            ('10003', '10005', 'category 1', self.creation_date),
            ('10004', '10005', 'category 2', self.creation_date),
        ]
        self.cursor.executemany(testing_categories, values)
        connection.commit()

        testing_data = '''INSERT INTO tasks (task_id, user_id, title, category_id, creation_date, date, completed, 
                        emailed, repeating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        values = [
            (10000, 10000, 'Buy potato', 10003, self.creation_date, None, 0, None, None),
            (10001, 10000, 'Buy carrot', 10003, self.creation_date, None, 0, None, None),
            (10003, 10002, 'Delete this task', None, self.creation_date, None, 1, None, None),
            (10004, 10002, 'Update date', None, self.creation_date, None, 0, None, None),
            (10005, 10002, 'Update completed', None, self.creation_date, None, 0, None, None),
            (10006, 10002, 'Update category', None, self.creation_date, None, 0, None, None),
            (10007, 10002, 'Update repeat', None, self.creation_date, None, 0, None, None),
            (10008, 10002, 'Update emailed', None, self.creation_date, None, 0, None, None),
        ]
        self.cursor.executemany(testing_data, values)
        connection.commit()

        self.database = Database()
        self.database.initialize(connection)
        self.connection = connection

    # Тесты пользователей
    def test_add_user(self):
        email = 'test2@gmail.com'
        password = 'not_strong_password'
        id = str(hash((email, password, self.reg_date)))
        self.database.add_user(id=id, email=email, password=password, registration_date=self.reg_date)

        check_user = '''SELECT * FROM users WHERE id = %s'''
        self.cursor.execute(check_user, [id])
        result = self.cursor.fetchall()

        expected = [(id, 'test2@gmail.com', 'not_strong_password', self.reg_date)]

        self.assertEqual(expected, result)

    def test_get_user(self):
        result = self.database.get_user(user_id='10000')
        expected = [('10000', 'get_me@gmail.com', 'very_strong_password', self.reg_date)]
        self.assertEqual(expected, result)

    def test_get_user_by_email(self):
        result = self.database.get_user_by_email(email='get_me@gmail.com')
        expected = [('10000', 'get_me@gmail.com', 'very_strong_password', self.reg_date)]
        self.assertEqual(expected, result)

    def test_delete_user(self):
        self.database.delete_user('10001')

        check_user = '''SELECT * FROM users WHERE id = "10001"'''
        self.cursor.execute(check_user)
        result = self.cursor.fetchall()

        self.assertEqual(0, len(result))

    def test_update_user_email(self):
        self.database.update_user(user_id='10003', email="changed@gmail.com", password='password')

        check_user = '''SELECT * FROM users WHERE id = "10003"'''
        self.cursor.execute(check_user)
        result = self.cursor.fetchall()

        expected = [('10003', 'changed@gmail.com', 'password', self.reg_date)]
        self.assertEqual(expected, result)

    def test_update_user_password(self):
        self.database.update_user(user_id='10004', email="change_my_password@mail.ru", password='changed_password')

        check_user = '''SELECT * FROM users WHERE id = "10004"'''
        self.cursor.execute(check_user)
        result = self.cursor.fetchall()

        expected = [('10004', 'change_my_password@mail.ru', 'changed_password', self.reg_date)]
        self.assertEqual(expected, result)

    # Тесты категорий
    def test_get_category(self):
        result = self.database.get_category(category_id='10000')
        expected = [('10000', '10002', 'get this task', self.creation_date)]
        self.assertEqual(expected, result)

    def test_get_categories_list(self):
        result = self.database.get_categories_list(user_id='10005')
        expected = [
            ('10003', '10005', 'category 1', self.creation_date),
            ('10004', '10005', 'category 2', self.creation_date),
        ]
        self.assertEqual(expected, result)

    def test_add_category(self):
        id = str(hash(('10002', 'add task', self.creation_date)))
        self.database.add_category(category_id=id, user_id='10002', title='add task', creation_date=self.creation_date)

        check_category = '''SELECT category_id, user_id, title, creation_date FROM categories WHERE category_id = %s'''
        self.cursor.execute(check_category, [(id)])
        result = self.cursor.fetchall()

        expected = [(id, '10002', 'add task', self.creation_date)]
        self.assertEqual(expected, result)

    def test_delete_category(self):
        self.database.delete_category(category_id='10001')

        check_category = '''SELECT * FROM categories WHERE category_id = "10001"'''
        self.cursor.execute(check_category)
        result = self.cursor.fetchall()

        self.assertEqual(0, len(result))

    def test_update_category_title(self):
        self.database.update_category(category_id=10002, title='updated title')

        check_category = '''SELECT category_id, user_id, title, creation_date FROM categories 
                         WHERE category_id = "10002"'''
        self.cursor.execute(check_category)
        result = self.cursor.fetchall()

        expected = [('10002', '10002', 'updated title', self.creation_date)]
        self.assertEqual(expected, result)

    # Тесты задач
    def test_get_task(self):
        result = self.database.get_task(task_id=10000)
        expected = [('10000', '10000', 'Buy potato', '10003', self.creation_date, None, 0, None, None)]
        self.assertEqual(expected, result)

    def test_get_users_tasks(self):
        result = self.database.get_users_tasks(user_id=10000)
        expected = [
            ('10000', '10000', 'Buy potato', '10003', self.creation_date, None, 0, None, None),
            ('10001', '10000', 'Buy carrot', '10003', self.creation_date, None, 0, None, None)
        ]
        self.assertEqual(expected, result)

    def test_get_category_task(self):
        result = self.database.get_category_tasks(category_id='10003')
        expected = [
            ('10000', '10000', 'Buy potato', '10003', self.creation_date, None, 0, None, None),
            ('10001', '10000', 'Buy carrot', '10003', self.creation_date, None, 0, None, None)
        ]
        self.assertEqual(expected, result)

    def test_add_default_task(self):
        date = str(datetime(2022, 10, 10, 12, 0))
        self.database.add_task(task_id=10137,
                               user_id=10002,
                               title='Play Stray',
                               category_id=10004,
                               creation_date=self.creation_date,
                               date=date)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                     emailed, repeating FROM tasks WHERE task_id = 10137'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10137', '10002', 'Play Stray', '10004', self.creation_date,
                     date, 0, None, None)]
        self.assertEqual(expected, result)

    def test_add_full_task(self):
        date = str(datetime(2022, 10, 10, 12, 0))
        self.database.add_task(task_id=10138,
                               user_id=10002,
                               title='Play Humankind',
                               creation_date=self.creation_date,
                               category_id=10004,
                               completed=1,
                               date=date,
                               repeating=100,
                               emailed=0)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                             emailed, repeating FROM tasks WHERE task_id = 10138'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10138', '10002', 'Play Humankind', '10004', self.creation_date,
                     date, 1, 0, 100)]
        self.assertEqual(expected, result)

    def test_delete_task(self):
        self.database.delete_task(task_id=10003)
        check_task = '''SELECT * FROM tasks WHERE task_id = 10003'''
        self.cursor.execute(check_task)
        self.assertEqual(0, len(self.cursor.fetchall()))

    def test_update_task_title(self):
        self.database.update_task(task_id=10001,
                                  title='Buy parrot',
                                  category_id=10003,
                                  date=None,
                                  completed=0,
                                  repeating=None,
                                  emailed=None)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                     emailed, repeating FROM tasks WHERE task_id = 10001'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10001', '10000', 'Buy parrot', '10003', self.creation_date, None, 0, None, None)]
        self.assertEqual(expected, result)

    def test_update_task_date(self):
        date = str(datetime(2022, 6, 9, 17, 13))
        self.database.update_task(task_id=10004,
                                  title='Update date',
                                  category_id=None,
                                  date=date,
                                  repeating=None,
                                  completed=0,
                                  emailed=None)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                     emailed, repeating FROM tasks WHERE task_id = 10004'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10004', '10002', 'Update date', None, self.creation_date, date, 0, None, None)]
        self.assertEqual(expected, result)

    def test_update_completed(self):
        self.database.update_task(task_id=10005,
                                  category_id=None,
                                  title='Update completed',
                                  date=None,
                                  completed=1,
                                  repeating=None,
                                  emailed=None)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                     emailed, repeating FROM tasks WHERE task_id = 10005'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10005', '10002', 'Update completed', None, self.creation_date, None, 1, None, None)]
        self.assertEqual(expected, result)

    def test_update_category(self):
        self.database.update_task(task_id=10006,
                                  title='Update category',
                                  category_id=None,
                                  date=None,
                                  repeating=None,
                                  completed=0,
                                  emailed=None)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                             emailed, repeating FROM tasks WHERE task_id = 10006'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10006', '10002', 'Update category', None, self.creation_date, None, 0, None, None)]
        self.assertEqual(expected, result)

    def test_update_repeating(self):
        self.database.update_task(task_id=10007,
                                  title='Update repeat',
                                  category_id=None,
                                  date=None,
                                  repeating=15,
                                  completed=0,
                                  emailed=None)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                             emailed, repeating FROM tasks WHERE task_id = 10007'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10007', '10002', 'Update repeat', None, self.creation_date, None, 0, None, 15)]
        self.assertEqual(expected, result)

    def test_update_emailed(self):
        self.database.update_task(task_id=10008,
                                  title='Update emailed',
                                  category_id=None,
                                  date=None,
                                  repeating=None,
                                  completed=0,
                                  emailed=1)
        check_task = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                             emailed, repeating FROM tasks WHERE task_id = 10008'''
        self.cursor.execute(check_task)
        result = self.cursor.fetchall()
        expected = [('10008', '10002', 'Update emailed', None, self.creation_date, None, 0, 1, None)]
        self.assertEqual(expected, result)

    @classmethod
    def tearDownClass(cls):
        cls.database.clean_testing_data()
        cls.database.close()


if __name__ == '__main__':
    unittest.main()