from main import app
from models import *
from flask_testing import TestCase
import unittest

from io import BytesIO


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        manager2 = User('Kousaka', 'Honoka', 'honoka@takamachi.com', 'honoka')
        manager2.set_user_manager()
        user5 = User('Yazawa', 'Nico', 'nico@takamachi.com', 'nico1234')
        user5.set_user_buyer()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        db.session.add(Process_List('making cheese', 'Cheese making process'))

        db.session.commit()
        # add a manager account and a random contact form entry

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class Manager_role(BaseTestCase):


    # Test if an actual manager can log in.
    def test_maanger_login(self):
        print('\n## Testing if a manager could log into system. ##')
        response = self.manager_login('honoka@takamachi.com', 'honoka', 'M')
        self.assertIn(b'Hello, Manager Honoka.', response.data)


    # Test if a non-manager user can log in.
    def test_non_manager_login(self):
        print('\n## Testing if a non-manager could log into system. ##')
        response = self.manager_login('nico@takamachi.com', 'nico1234', 'B')
        self.assertIn(b'Sorry, you are not a manager.', response.data)


    def manager_login(self, email, password, type):
        return self.client.post('/manager_login', data=dict(
            email=email,
            password=password,
            type='M',
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
