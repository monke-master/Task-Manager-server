from unittest import *
from main import Application


class TestApplication(TestCase):
    application = None
    flask_app = None

    def setUpClass(self) -> None:
        self.application = Application()
        self.application.initialize()
        self.application.app.config['TESTING'] = True
        self.flask_app = self.application.app.test_client()

    def test_get_user(self):
        result = self.flask_app.get('/user/1')
        expected = {}

    def tearDownClass(self) -> None:
        self.application.clean_db()