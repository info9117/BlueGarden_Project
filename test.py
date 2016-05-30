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
        user2 = User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins')
        user2.set_user_farmer()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(user2)
        db.session.add(User('Master', 'Farmer', 'mrmf@gmail.com', 'shazza'))
        db.session.add(Unit('Kg'))
        db.session.add(Unit('gm'))
        db.session.add(Unit('l'))
        db.session.add(Unit('ml'))
        db.session.flush()
        db.session.add(Address('123 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Address('126 Hill Rd', None, 'Melbourne', 'NSW', 'Australia', 2010))
        db.session.flush()
        db.session.add(Farm('Shire Farms', 1))
        db.session.add(Farm('Mordor Farms', 1))
        db.session.add(Produce('corn', 'vegetable', 'tasty', 1, 1))
        db.session.add(Produce('milk', 'dairy', 'yum', 2, 2))
        db.session.flush()
        db.session.add(Price(1, 1, 2.2))
        db.session.add(Price(2, 1, 4.4))
        db.session.add(RecentProduce(1, 1))
        db.session.flush()
        db.session.add(Works(2, 1))
        db.session.add(Works(2, 2))
        db.session.flush()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BlueGardenTestCase(BaseTestCase):

    produce_added = False

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


    #Testing add crop with new crop
    def test_login_addcrop(self):
        print('\n## Testing add crop with new crop')

        #rv=self.login('singarisathwik007@gmail.com', 'dm08b048')
        #rv=self.addcrop('1', 'corn', 'plant', '1')

        rv = self.login('singarisathwik007@gmail.com', 'dm08b048')
        rv = self.addcrop('563', 'corn', 'harvest', '892')

        assert b'You success added crop' in rv.data


    def test_dashboard_recently_viewed(self):
        print('\n## Testing viewing recently viewed on the dashboard')
        rv = self.login('singarisathwik007@gmail.com', 'dm08b048')
        assert b'corn' in rv.data

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



    # Test add crop function    

    def addcrop(self,id, cropname, growstate, farmid):
        
        return self.client.post('/addcrop',data=dict(
            id = id,
            crop_name = cropname,
            grow_state = growstate,
            farm_id = farmid
            ),follow_redirects=True)

    '''#Test change crop state
    def change_state(self, cropid, changestate):
        return self.client.post('/change_state/1',data=dict(
            oristate = Crop.query.get(cropid), 
            new_state=changestate), follow_redirects=True)

    #Test change crop state       
    def test_change_state(self):
        rv=self.login('singarisathwik007@gmail.com', 'dm08b048')
        rv=self.change_state('1','harvest')
        assert b'you successfully change the state' in rv.data'''


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
        self.login('bbaggins@lotr.com', 'bilbobaggins')
        response = self.client.get('/farm/1/produce/add', content_type='html/text', follow_redirects=True)
        self.assertIn(b'Shire Farms', response.data)
       

    # Products details test
    def test_view_produce_page_content(self):
        print('\n## Testing produce details page content ##')
        response = self.client.get('/produce/1', content_type='html/text')
        self.assertIn(b'corn', response.data)
        self.assertIn(b'2.2', response.data)
        self.assertIn(b'Shire Farms', response.data)
        

    def test_adding_produce_to_farm(self):
        print('\n## Testing Add produce to farm ##')
        self.login('bbaggins@lotr.com', 'bilbobaggins')
        response = self.add_produce('Eggplant', 'Big eggplants', 'Vegetable', 1, 4.38, 'static/images/eggplant.jpg', 1)
        self.assertIn(b"Success", response.data)

    def add_produce(self, name, description, category, selected_units, price1, prod_image, farm_id):
        img = open(prod_image, 'rb')
        try:
            img_bytes_io = BytesIO(img.read())
            filename = img.name
            post_data = {
                'name': name, 'description': description, 'category': category,
                'units': selected_units,
                'price1': price1,
            }
            for key, val in post_data.items():
                if not isinstance(val, str):
                    post_data[key] = str(val)
            post_data['prod_image'] = (img_bytes_io, filename)
        finally:
            img.close()
        return self.client.post('/farm/'+str(farm_id)+'/produce/add', content_type='multipart/form-data',
                                data=post_data, follow_redirects=True)

    def test_browse_produce_content(self):
        print('\n## Testing browse produce page content ##')
        self.login('bbaggins@lotr.com', 'bilbobaggins')
        if not self.produce_added:
            self.add_test_produce()
        response = self.client.get('/search/produce', follow_redirects=True)
        self.assertIn(b'Broccoli', response.data)

    def test_browse_produce_content_with_filter(self):
        print('\n## Testing browse produce page content with filters ##')
        self.login('bbaggins@lotr.com', 'bilbobaggins')
        if not self.produce_added:
            self.add_test_produce()
        response = self.client.get('/search/produce?vegetable=on&location=Sydney', follow_redirects=True)
        self.assertNotIn(b'Apple', response.data)

    def add_test_produce(self):
        self.add_produce('Apple', 'Big Apples', 'Fruit', 1, 4.38, 'static/images/apples.jpg', 1)
        self.add_produce('Banana', 'Big Bananas', 'Fruit', 1, 4.38, 'static/images/banana.jpg', 1)
        self.add_produce('Broccoli', 'Big Broccoli', 'Vegetable', 1, 4.38, 'static/images/broccoli.jpg', 2)
        self.add_produce('Carrots', 'Big Carrots', 'Vegetable', 1, 4.38, 'static/images/carrots.jpg', 2)
        self.add_produce('Orange', 'Big Oranges', 'Fruit', 1, 4.38, 'static/images/oranges.jpg', 1)
        self.add_produce('Potato', 'Big Potatoes', 'Vegetable', 1, 4.38, 'static/images/potato.jpg', 2)
        self.produce_added = True

    # Testing the flag for farmer user type
    def test_farmer_type(self):
        print('\n## Testing the flag for farmer user type ##')
        user = User.query.filter_by(email='mrmf@gmail.com').first()
        User.set_user_farmer(user)
        assert 'Master' in [farmer.first_name for farmer in User.query.filter_by(type='C').all()]
        user.type = 'B'
        assert 'Master' not in [farmer.first_name for farmer in User.query.filter_by(type='C').all()]

    # Testing new farmer user has no farms yet
    def test_farm_page_content(self):
        print('\n## Testing new farmer user has no farms yet ##')
        self.login('mrmf@gmail.com', 'shazza')
        response = self.client.get('/sell', follow_redirects=True)
        self.assertIn(b"You dont have any farms yet.",response.data)

    # Testing that user can add farms that they work on
    def test_add_farms(self):
        print('\n## Testing that user can add farms that they work on ##')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Community Farm",response.data)

    def test_add_duplicate_farms(self):
        print('\n## Testing that user cannot add duplicate farms that they work on ##')
        self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Already Exists",response.data)

    def add_farm(self, name, address1, address2, city, state, country, postcode):
        self.login('mrmf@gmail.com', 'shazza')
        return self.client.post('/sell', data=dict(
            name=name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            country=country,
            postcode=postcode
        ), follow_redirects=True)
        
    def add_activity(self, description,field,date,resource):
        self.login('mrmf@gmail.com', 'shazza')
        return self.client.post('/activity', data=dict(
            description=description,
            field=field,
            date=date,
            resource=resource
        ), follow_redirects=True)


    #Testing that user can record activities to their farm
    def test_add_activity(self):
        print('\n## Testing that user can record activities to their farm ##')
        self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        farm_id = 1
        db.session.add(Field('west block', 'Shire Farms', farm_id))
        db.session.add(Resource('fertiliser',farm_id))
        db.session.commit()        
        field = Field.query.filter_by(farm_id=farm_id).first()
        resource = Resource.query.filter_by(farm_id=farm_id).first()
        date = '3 May, 2016'
        description = 'Mowing the lawn'
        response = self.add_activity(description,field,date,resource)
        self.assertIn(b"Activity was recorded",response.data)        


    def test_add_to_cart(self):
        response = self.client.post('/produce/1', data=dict(
            amount='2'))
        self.assertIn(b'4.4', response.data)


if __name__ == '__main__':
    unittest.main()
