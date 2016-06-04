from main import app
from models import *
from flask_testing import TestCase
import unittest

class BlueGardenFarmTests(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        user2 = User('Bilbo', 'Baggins', 'bbaggins@lotr.com', 'bilbobaggins')
        user2.set_user_farmer()
        db.session.add(User('Sathwik', 'Singari', 'singarisathwik007@gmail.com', 'dm08b048'))
        db.session.add(user2)
        user3 = User('Master', 'Farmer', 'mrmf@gmail.com', 'shazza')
        user4 = User('Not', 'Farmer', 'mrmf@farm.com', 'qwerty')
        db.session.add(user3)
        db.session.add(user4)
        db.session.add(Address('123 Hill Rd', None, 'Sydney', 'NSW', 'Australia', 2010))
        db.session.add(Address('126 Hill Rd', None, 'Melbourne', 'NSW', 'Australia', 2010))
        db.session.flush()
        db.session.add(Farm('Shire Farms', 1))
        db.session.add(Farm('Mordor Farms', 1))
        db.session.flush()
        db.session.add(Works(2, 1))
        db.session.add(Works(2, 2))
        db.session.add(Activity_List('activity name',1))
        db.session.flush()
        db.session.add(Resource_List('fertiliser'))
        db.session.flush()
        db.session.add(Process_List('making cheese', 'Cheese making process'))
        db.session.add(Field("east block",'Shire Farms',1))
        db.session.add(Works(3, 1))
        user3.set_user_farmer()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #Testing resource list
    def test_login_resourcelist(self):
        print('\n## Testing add resource ##')
        rv = self.login('singarisathwik007@gmail.com', 'dm08b048')
        response = self.add_resourcelist('this is your resource')
        self.assertIn(b'this is your resource',response.data)

    def add_resourcelist(self, decription):
        self.login('mrmf@gmail.com', 'shazza')
        return self.client.post('/addresource', data = dict(
            resourcedescription = decription
        ), follow_redirects = True)

    # Testing add crop with new crop
    def test_login_addcrop(self):
        print('\n## Testing add crop with new crop')
        self.login('singarisathwik007@gmail.com', 'dm08b048')
        rv = self.addcrop('563', 'corn', 'harvest', '892')
        assert b'You success added crop' in rv.data

    # Test add crop function
    def addcrop(self, id, cropname, growstate, farmid):
        return self.client.post('/addcrop', data=dict(
            id=id,
            crop_name=cropname,
            grow_state=growstate,
            farm_id=farmid
        ), follow_redirects=True)

    # Test change crop state
    def change_state(self, cropid, changestate):
        return self.client.post('/change_state/1',data=dict(
            oristate = Crop.query.get(cropid),
            new_state=changestate), follow_redirects=True)

    # Test change crop state
    def test_change_state(self):
        rv=self.login('singarisathwik007@gmail.com', 'dm08b048')
        rv=self.change_state('1','harvest')
        assert b'you successfully change the state' in rv.data

    # Testing the flag for farmer user type
    def test_farmer_type(self):
        print('\n## Testing the flag for farmer user type ##')
        user = User.query.filter_by(email='mrmf@gmail.com').first()
        User.set_user_farmer(user)
        assert 'Master' in [farmer.first_name for farmer in User.query.filter_by(type='C').all()]
        user.type = 'B'


    # Testing new farmer user has no farms yet
    def test_farm_page_content(self):
        print('\n## Testing new farmer user has no farms yet ##')
        self.login('mrmf@farm.com', 'qwerty')
        response = self.client.get('/farm', follow_redirects=True)
        self.assertIn(b"You dont have any farms yet.", response.data)


    # Testing that user can add farms that they work on
    def test_add_farms(self):
        print('\n## Testing that user can add farms that they work on ##')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Community Farm", response.data)

    # Testing duplicate farm names error
    def test_add_duplicate_farms(self):
        print('\n## Testing that user cannot add duplicate farms that they work on ##')
        self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        response = self.add_farm('Community Farm', '1 First St', '', 'Camperdown', 'NSW', 'Aus', '2009')
        self.assertIn(b"Already Exists", response.data)


    def add_farm(self, name, address1, address2, city, state, country, postcode):
        self.login('mrmf@gmail.com', 'shazza')
        return self.client.post('/farm', data=dict(
            name=name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            country=country,
            postcode=postcode
        ), follow_redirects=True)

    def add_process(self, process_name, process_description):
        self.login('mrmf@gmail.com', 'shazza')
        return self.client.post('/process', data=dict(
            process_name=process_name,
            process_description=process_description
        ), follow_redirects=True)

    def add_activity(self, process, description, resource, activity):
        self.login('mrmf@gmail.com', 'shazza')
        return self.client.post('/activity/0', data=dict(
            process=process,
            description=description,
            resource=resource,
            activity=activity
        ), follow_redirects=True)


    def start_process(self, target, farm, field, crop, date, user_id, process, other_target):
        return self.client.post('/active_process/process/1', data=dict(
            target=target,
            farm=farm,
            field=field,
            crop=crop,
            date=date,
            user_id=user_id,
            process=process,
            other_target=other_target
        ), follow_redirects=True)

     # Testing that farmer can register new process
    def test_add_process(self):
        print('\n## Testing that farmer can register new process ##')
        response = self.add_process( "Process name", "process_description")
        self.assertIn(b"Process name", response.data)

    # Testing process page errors
    def test_process_page(self):
        print('\n## Testing process page error: name ##')
        response = self.add_process("", "process_description")
        self.assertIn(b"You must enter a Process name", response.data)
        print('\n## Testing process page error: description ##')
        response = self.add_process("Process name", "")
        self.assertIn(b"You must enter a Process description", response.data)

    # Testing that user can record activities
    def test_add_activity(self):
        print('\n## Testing that user can record activities ##')
        process = db.session.query(Process_List).order_by(Process_List.id.asc()).first().id
        resource = db.session.query(Resource_List).order_by(Resource_List.id.asc()).first().id
        description = 'Mowing the lawn'
        response = self.add_activity(process, description, resource,'')
        self.assertIn(b"was added to", response.data)

    # Testing that farmer can reuse existing activities in process template
    def test_add_existing_activity(self):
        print('\n## Testing that farmer can reuse existing activities in process template ##')
        response = self.add_activity(1, '', '', 1)
        self.assertIn(b"Activity was recorded", response.data)

    # Testing activity page errors
    def test_activity_page_errors(self):
        print('\n## Testing activity page errors ##')
        response = self.add_activity(1, 'activity decrpn', '', '')
        self.assertIn(b"select a resource this time", response.data)
        response = self.add_activity('', 'plough field', 1, '')
        self.assertIn(b"select a process", response.data)
        response = self.add_activity(1, '', 1, '')
        self.assertIn(b"add an activity description", response.data)

    # Testing that farmer can initiate new process on target <X>
    def test_start_process(self):
        self.login('mrmf@gmail.com', 'shazza')
        user = User.query.get(User.query.filter_by(email='mrmf@gmail.com').first().id)
        print('\n## Test-- Farmer starts process for: Farm ##')
        response = self.start_process("farm", 1, '', '', "10 Sep, 2016", user.id, 1, '')
        self.assertIn(b"for your farm", response.data)
        print('\n## Test-- Farmer starts process for: Other ##')
        response = self.start_process("other", '', '', '', "10 Sep, 2016", user.id, 1, 'On the roof!')
        self.assertIn(b"for your other", response.data)
        print('\n## Test-- Farmer starts process for: None ##')
        response = self.start_process('', '', '', '', "10 Sep, 2016", user.id, 1, '')
        self.assertIn(b"commences on the ", response.data)
        print('\n## Test-- Farmer starts process for: Field ##')
        response = self.start_process("field", '', 1, '', "10 Sep, 2016", user.id, 1, '')
        self.assertIn(b"for your field", response.data)
        print('\n## Test-- Farmer starts process for: Crop ##')
        self.add_activity(1, "step in process", 1,'') # test active activity instance
        response = self.start_process("crop", '', '', 1, "10 Sep, 2016", user.id, 1, '')
        self.assertIn(b"for your crop", response.data)

    # Testing redirect to start process for crop
    def test_start_crop_process(self):
        self.login('mrmf@gmail.com', 'shazza')
        print('\n## testing redirect to start process for crop ##')
        response = self.client.get('/active_process/crop/1')
        self.assertIn(b'Start a new Process',response.data)
        self.assertIn(b'crop', response.data)


    # Testing that farmer can see process targets in DDlist
    def test_farmers_targets(self):
        print('\n## Testing that farmer can see process targets in DDlist ##')
        self.login('mrmf@gmail.com', 'shazza')
        response = self.start_process("field", '', '', '', '', 3, '', '')# Why error?
        self.assertIn(b"east block", response.data)


    # Testing that errors are displayed when adding a farm without name or address
    def test_add_farm_errors(self):
        print('\n## Testing that farmer cannot add nameless farm ##')
        response = self.add_farm('name', '', '', '', '', '', '')
        self.assertIn(b"You must enter an address", response.data)
        print('\n## Testing that farmer cannot add addressless farm ##')
        response = self.add_farm('', 'address1', '', '', '', '', '')
        self.assertIn(b"You must enter a name", response.data)


    # testing farmer can add activity to process template
    def test_process_template_build(self):
        self.login('mrmf@gmail.com', 'shazza')
        print('\n## Testing that user can record steps in process ##')
        response = self.client.post('/activity/1', data=dict(
            process=1,
            description="step1",
            resource=1
        ), follow_redirects=True)
        self.assertIn(b"was added to making cheese", response.data)


    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

if __name__ == '__main__':
    unittest.main()