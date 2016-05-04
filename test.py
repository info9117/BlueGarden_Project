from main import app
from shared import db
from models import *
from flask_testing import TestCase
import unittest
from io import StringIO, BytesIO


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        db.session.add(Address('123 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Address('126 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Farm('Shire Farms', 1))
        db.session.add(Farm('Mordor Farms', 2))
        db.session.add(Image('produce/1/eggplant.jpeg'))
        db.session.add(Produce('Eggplant', 'Sweet organic eggplants', 'Vegetable', 1))
        db.session.add(Price(1, 1, 4.35))
        db.session.add(Price(1, 2, 2.8))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BlueGardenTestCase(BaseTestCase):
    # Testing the home page content
    def test_index_content(self):
        print('\n## Testing Home page for welcome message ##')
        response = self.client.get('/', content_type='html/text')
        self.assertIn(b'Welcome to Blue Garden', response.data)

    # Testing Login page content
    def test_login_page_content(self):
        response = self.client.get('/login', content_type='html/text')
        print('\n## Testing Login page for content ##')
        self.assertIn(b"""Don't have an account? <a href="/register">Register</a>""", response.data)

    # Testing Login with valid credentials
    def test_login_valid_credentials(self):
        print('\n## Testing Login page with valid credentials ##')
        response = self.login('singarisathwik007@gmail.com', 'dm08b048')
        self.assertIn(b'Hello Sathwik', response.data)

    # Testing Login with invalid credentials
    def test_login_invalid_credentials(self):
        print('\n## Testing Login page with invalid credentials ##')
        response = self.login('singarisathwik007@gmail.com', 'dm08b48')
        self.assertIn(b'Email Id/Password do not match', response.data)

    # Testing Logout
    def test_logout(self):
        print('\n## Testing logout ##')
        response = self.logout()
        self.assertIn(b'You successfully logged out', response.data)

    # Testing Registration Page content
    def test_register_page_content(self):
        response = self.client.get('/register', content_type='html/text')
        print('\n## Testing Registration page for content ##')
        self.assertIn(b"""Already have an account? <a href="/login">Log In</a>""", response.data)

    # Testing Registration with existing credentials
    def test_register_existing_credentials(self):
        print('\n## Testing Register page with existing credentials ##')
        response = self.register('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048')
        self.assertIn(b'Email Id already exists', response.data)

    # Testing Registration with valid credentials
    def test_register_valid_credentials(self):
        print('\n## Testing Register page with valid credentials ##')
        response = self.register('Frodo', 'Baggins', 'fbaggins@lotr.com', 'frodobaggins')
        self.assertIn(b'Hello Frodo', response.data)

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def register(self, first_name, last_name, email, password):
        return self.client.post('/register', data=dict(
            firstname=first_name,
            lastname=last_name,
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_dashboard_for_content(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['email'] = 'singarisathwik007@gmail.com'
                session['firstname'] = 'Sathwik'
                session['lastname'] = 'Singari'
                print('\n## Testing dashboard page for content ##')

        response = self.client.get('/dashboard', content_type='html/text')
        self.assertIn(b'Hello Sathwik', response.data)

    def test_add_produce_page_content(self):
        print('\n## Testing Add produce page content ##')
        with self.client as c:
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['email'] = 'singarisathwik007@gmail.com'
                session['firstname'] = 'Sathwik'
                session['lastname'] = 'Singari'
        response = self.client.get('/farm/1/produce/add', content_type='html/text')
        self.assertIn(b'Shire Farms', response.data)

    def test_adding_produce_to_farm(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['logged_in'] = True
                session['email'] = 'singarisathwik007@gmail.com'
                session['firstname'] = 'Sathwik'
                session['lastname'] = 'Singari'
        response = self.add_produce('Eggplant', 'Big eggplants', 'Vegetable', 1, 4.38, 'static/images/eggplant.jpeg')
        self.assertIn(b"Success", response.data)

    def add_produce(self, name, description, category, selected_units, price1, prod_image):
        with open(prod_image, 'rb') as img:
            img_bytes_io = BytesIO(img.read())
            post_data = {
                'name': name, 'description': description, 'category': category,
                'units': selected_units,
                'price1': price1,
            }
            for key, val in post_data.items():
                if not isinstance(val, str):
                    post_data[key] = str(val)
            post_data['prod_image'] = (img_bytes_io, 'eggplant.jpeg')
            return self.client.post('/farm/2/produce/add', content_type='multipart/form-data',
                                    data=post_data)


if __name__ == '__main__':
    unittest.main()
