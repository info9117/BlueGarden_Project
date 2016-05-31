from main import app
from models import *
from flask_testing import TestCase
import unittest


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BlueGardenTestCase(BaseTestCase):

    # Testing Registration Page content
    def test_register_page_content(self):
        response = self.client.get('/register', content_type='html/text')
        print('\n## Testing Registration page for content ##')
        self.assertIn(b"""Already have an account? <a href="/login">Log In</a>""", response.data)

    def test_password_with_digits_only(self):
        print('\n## Testing Registration with digits only password ##')
        response = self.register('Shirasaki', 'Tsugumi', 'shirasaki@takamachi.com', '223355668899')
        self.assertIn(b"Password cannot contain only numbers. >_<", response.data)

    def test_short_password(self):
        print('\n## Testing Registration with too short password ##')
        response = self.register('Shirasaki', 'Tsugumi', 'shirasaki@takamachi.com', '2atr')
        self.assertIn(b'Password is too short! -_-##', response.data)

    def test_good_password(self):
        print('\n## Testing Registration with good password ##')
        response = self.register('Shirasaki', 'Tsugumi', 'shirasaki@takamachi.com', 'rqweERBC9807')
        self.assertIn(b'Hello, Shirasaki', response.data)

    def register(self, first_name, last_name, email, password):
        return self.client.post('/register', data=dict(
            firstname=first_name,
            lastname=last_name,
            email=email,
            password=password
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
