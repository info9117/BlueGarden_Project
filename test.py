from main import app
from shared import db
from models.user import User
from flask_testing import TestCase
import unittest


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BlueGardenTestCase(BaseTestCase):
    # Testing the home page content
    def test_index_content(self):
        response = self.client.get('/', content_type='html/text')
        with self.client as c:
            with c.session_transaction() as session:
                if session.get('logged_in', False):
                    print('\n## Testing Home page for content ##')
                    print('\n## User already logged in. So verifying dashboard ##')
                    self.assertIn(b'Hello ' + session['firstname'], response.data)
                else:
                    print('\n## Testing Home page for welcome message ##')
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
        print(type(response))
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
    
    #Testing the flag for farmer user type
    def test_farmer_type(self):
        print('\n## Testing the flag for farmer user type ##')
        user = User.query.filter_by(email='singarisathwik007@gmail.com').first()
        User.set_user_farmer(user)
        assert User.query.filter_by(type='C').first().first_name == 'Sathwik'
        user.type = 'B'
        assert not User.query.filter_by(email='singarisathwik007@gmail.com').first().type == 'C'

    #Testing new farmer user has no farms yet
    def test_farm_page_content(self):
        print('\n## Testing new farmer user has no farms yet ##')
        self.login('singarisathwik007@gmail.com', 'dm08b048')
        response = self.client.get('/sell', follow_redirects=True)
        self.assertIn(b"You dont have any farms yet.",response.data)
        
    #Testing that user can add farms that they work on
    def test_add_farms(self):
        print('\n## Testing that user can add farms that they work on ##')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Community Farm",response.data)
        
    def add_farm(self, name, address1, address2, city, state, country, postcode):
        self.login('singarisathwik007@gmail.com', 'dm08b048')
        return self.client.post('/sell', data=dict(
            name=name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            country=country,
            postcode=postcode
        ), follow_redirects=True)        

if __name__ == '__main__':
    unittest.main()
