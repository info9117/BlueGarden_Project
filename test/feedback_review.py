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
        db.session.add(User('Kousaka', 'Honoka', 'kousaka.honoka@icloud.com', 'admin678kousaka'))
        db.session.add(Contact('Hey!', 'I have something to say ^_^', ))
        db.session.flush()
        db.session.commit()
        # add a manager account and a random contact form entry

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

    # Testing add crop with new crop
    def test_login_addcrop(self):
        print('\n## Testing add crop with new crop')
        rv = self.login('singarisathwik007@gmail.com', 'dm08b048')
        rv = self.addcrop('563', 'corn', 'harvest', '892')
        assert b'You success added crop' in rv.data

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

    def addcrop(self, id, cropname, growstate, farmid):
        return self.client.post('/addcrop', data=dict(
            id=id,
            crop_name=cropname,
            grow_state=growstate,
            farm_id=farmid
        ), follow_redirects=True)

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
        self.login('singarisathwik007@gmail.com', 'dm08b048')
        response = self.client.get('/farm/1/produce/add', content_type='html/text', follow_redirects=True)
        self.assertIn(b'Shire Farms', response.data)

    def test_adding_produce_to_farm(self):
        print('\n## Testing Add produce to farm ##')
        self.login('singarisathwik007@gmail.com', 'dm08b048')
        response = self.add_produce('Eggplant', 'Big eggplants', 'Vegetable', 1, 4.38, 'static/images/eggplant.jpg')
        self.assertIn(b"Success", response.data)

    def add_produce(self, name, description, category, selected_units, price1, prod_image):
        img = open(prod_image, 'rb')
        try:
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
        finally:
            img.close()
        return self.client.post('/farm/1/produce/add', content_type='multipart/form-data',
                                data=post_data)

    # Testing the flag for farmer user type
    def test_farmer_type(self):
        print('\n## Testing the flag for farmer user type ##')
        user = User.query.filter_by(email='singarisathwik007@gmail.com').first()
        User.set_user_farmer(user)
        assert User.query.filter_by(type='C').first().first_name == 'Sathwik'
        user.type = 'B'
        assert not User.query.filter_by(email='singarisathwik007@gmail.com').first().type == 'C'

    # Testing new farmer user has no farms yet
    def test_farm_page_content(self):
        print('\n## Testing new farmer user has no farms yet ##')
        self.login('singarisathwik007@gmail.com', 'dm08b048')
        response = self.client.get('/sell', follow_redirects=True)
        self.assertIn(b"You dont have any farms yet.", response.data)

    # Testing that user can add farms that they work on
    def test_add_farms(self):
        print('\n## Testing that user can add farms that they work on ##')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Community Farm", response.data)

    # Testing that user cannot add duplicate farms that they work on
    def test_add_duplicate_farms(self):
        print('\n## Testing that user cannot add duplicate farms that they work on ##')
        self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Already Exists", response.data)

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


# test case to check if contact form system works.
'''    def test_contact_form(self):
        print('\n## Testing that guest can fill contact form and set it to system ##')
        response = self.contact('New Enquiry Test', 'Hello. I have something to share. ^_^')
        self.assertIn(b'Congrats! Your enquiry has been sent! ', response.data)
'''
if __name__ == '__main__':
    unittest.main()
