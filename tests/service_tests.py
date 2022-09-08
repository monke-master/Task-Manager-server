from unittest import *
from database_service import *

class ServiceTest(TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.service = DatabaseService()

    def test_get_existing_user(self):
        result = self.service.get_user(1)
        expected = ({
                'id': '1',
                'email': 'testing@gmail.com',
                'password': 'password',
                'registration_date': '2022-08-11 13:04:00'
            }, 200)
        self.assertEqual(result, expected)

    def test_get_non_existing_user(self):
        result = self.service.get_user(1000)
        expected = 404
        self.assertEqual(result, expected)



    def test_add_user(self):
