from main import app
from shared import db
from models import *
from flask_testing import TestCase
import unittest


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User('Hayate', 'Yagami', 'hayate@microsoft.com', 'hayate1234'))  # This one is a normal user
        db.session.add(User('Nanoha', 'Takamachi', 'nanoha@microsoft.com', 'nanoha1234')) # This one is company manager
        db.session.add(Contact('Shirasaki', 'shirasaki@microsoft.com', 'Hey', 'I want to share something to you. '))
        db.session.add(Contact('Honoka', 'honoka@microsoft.com', 'Hello', 'I dont like something and I want to complain'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BlueGardenTestCase(BaseTestCase):

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

    # Products details test
    def test_view_produce_page_content(self):
        print('\n## Testing produce details page content ##')
        response = self.client.get('/produce/1', content_type='html/text')
        self.assertIn(b'Eggplant', response.data)
        self.assertIn(b'4.35', response.data)
        self.assertIn(b'Shire Farms', response.data)

    # Test if feedback form can be viewed properly. Case 1. Only manager can view content
    def test_view_feedback_page_content_case1(self):
        print('\n## Testing viewing feedback page content from authorised user##')
        with self.client as c:
            with c.session_view_feedback() as session:
                session['logged_in'] = True
                session['email'] = 'nanoha@microsoft.com'
                session['firstname'] = 'Nanoha'
                session['lastname'] = 'Takamachi'

        response = self.client.get('/feedback/portal', content_type='html/text')
        self.assertIn(b'Shirasaki', response.data)
        self.assertIn(b'shirasaki@microsoft.com', response.data)
        self.assertIn(b'Hey', response.data)
        self.assertIn(b'I want to share something to you. ', response.data)

    # Test if feedback form can be viewed properly. Case 2. Only manager can view content
    def test_view_feedback_page_content_case2(self):
        print('\n## Testing viewing feedback page content from authorised user##')
        with self.client as c:
            with c.session_view_feedback() as session:
                session['logged_in'] = True
                session['email'] = 'nanoha@microsoft.com'
                session['firstname'] = 'Nanoha'
                session['lastname'] = 'Takamachi'
        response = self.client.get('/feedback/portal', content_type='html/text')
        self.assertIn(b'Honoka', response.data)
        self.assertIn(b'honoka@microsoft.com', response.data)
        self.assertIn(b'Hello', response.data)
        self.assertIn(b'I dont like something and I want to complain', response.data)

    # Test if feedback can be viewed by non-manager user.
    def test_unauthorised_feedback_page_content_view(self):
        print('\n## Testing viewing feedback page content from unauthorised user##')
        with self.client as c:
            with c.session_view_feedback() as session:
                session['logged_in'] = True
                session['email'] = 'hayate@microsoft.com'
                session['firstname'] = 'Hayate'
                session['lastname'] = 'Yagami'
        response = self.client.get('login')

    def test_add_to_cart(self):
        response = self.client.post('/produce/1', data=dict(
            amount='2'))
        self.assertIn(b'8.7', response.data)


if __name__ == '__main__':
    unittest.main()
