import datetime

from mysql.connector import *


class Database:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def initialize(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    # Данные пользователя
    def get_user(self, user_id):
        query = '''SELECT * FROM users WHERE id = %s'''
        try:
            self.__cursor.execute(query, [user_id])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def get_user_by_email(self, email):
        query = '''SELECT * FROM users WHERE email = %s'''
        try:
            self.__cursor.execute(query, [email])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def add_user(self, id, email, password, registration_date):
        query = '''INSERT INTO users (id, email, password, registration_date) VALUES (%s, %s, %s, %s)'''
        try:
            values = (id, email, password, registration_date)
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def delete_user(self, user_id):
        query = '''DELETE FROM users WHERE id = %s'''
        try:
            self.__cursor.execute(query, [user_id])
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def update_user(self, user_id, email, password):
        query = '''UPDATE users SET email = %s, password = %s WHERE id = %s'''
        try:
            values = (email, password, user_id)
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    # Данные категории
    def add_category(self, category_id, user_id, title, creation_date):
        query = '''INSERT INTO categories (category_id, user_id, title, creation_date) VALUES (%s, %s, %s, %s)'''
        try:
            values = (category_id, user_id, title, creation_date)
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def get_category(self, category_id):
        query = '''SELECT category_id, user_id, title, creation_date FROM categories WHERE category_id = %s'''
        try:
            self.__cursor.execute(query, [category_id])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def get_categories_list(self, user_id):
        query = '''SELECT category_id, user_id, title, creation_date FROM categories WHERE user_id = %s'''
        try:
            self.__cursor.execute(query, [user_id])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def delete_category(self, category_id):
        query = '''DELETE FROM categories WHERE category_id = %s'''
        try:
            self.__cursor.execute(query, [category_id])
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def update_category(self, category_id, title):
        query = '''UPDATE categories SET title = %s WHERE category_id = %s'''
        try:
            values = (title, category_id)
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    # Данные задач
    def get_task(self, task_id):
        query = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                emailed, repeating FROM tasks WHERE task_id = %s'''
        try:
            self.__cursor.execute(query, [task_id])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def get_users_tasks(self, user_id):
        query = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                emailed, repeating FROM tasks WHERE user_id = %s'''
        try:
            self.__cursor.execute(query, [user_id])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def get_category_tasks(self, category_id):
        query = '''SELECT task_id, user_id, title, category_id, creation_date, date, completed, 
                emailed, repeating FROM tasks WHERE category_id = %s'''
        try:
            self.__cursor.execute(query, [category_id])
            return self.__cursor.fetchall()
        except Error as error:
            return error

    def add_task(self, task_id, user_id, title, creation_date, category_id=None, date=None, completed=0,
                 repeating=None, emailed=None):
        query = '''INSERT INTO tasks (task_id, user_id, title, category_id, creation_date, date, completed, 
                repeating, emailed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        try:
            values = (task_id, user_id, title, category_id, creation_date, date, completed, repeating, emailed)
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def delete_task(self, task_id):
        query = '''DELETE FROM tasks WHERE task_id = %s'''
        try:
            self.__cursor.execute(query, [task_id])
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def update_task(self, task_id, title, category_id, date, repeating, completed, emailed):
        query = '''UPDATE tasks SET title = %s, category_id = %s, date = %s, repeating = %s, completed = %s, 
                emailed = %s WHERE task_id = %s'''
        try:
            print(date)
            values = (title, category_id, date, repeating, completed, emailed, task_id)
            self.__cursor.execute(query, values)
            self.__connection.commit()
            return 200
        except Error as error:
            return error

    def close(self):
        self.__connection.close()
        self.__cursor.close()

    def clean_tables(self):
        clean_tasks_table = '''DELETE FROM tasks'''
        self.__cursor.execute(clean_tasks_table)
        clean_categories_table = '''DELETE FROM categories'''
        self.__cursor.execute(clean_categories_table)
        clean_users_table = '''DELETE FROM users'''
        self.__cursor.execute(clean_users_table)
        self.__connection.commit()

