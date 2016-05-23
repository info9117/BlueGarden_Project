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
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BlueGardenTestCase(BaseTestCase):

    # Testing empty contact form
    def test_empty_contact_form(self):
        print('\n## Testing Submitting with empty contact form ##')
        response = self.contact('', '', '', '') # empty name, empty email, empty title, empty enquiry
        self.assertIn(b'Missing compulsory fields', response.data)

    # Testing contact form with name only
    def test_name_only_contact_form(self):
        print('\n## Testing Submitting with empty contact form ##')
        response = self.contact('Nanoha', '', '', '') # empty name, empty email, empty title, empty enquiry
        self.assertIn(b'Missing compulsory fields', response.data)

    # Testing contact form with email only
    def test_email_only_contact_form(self):
        print('\n## Testing Submitting with empty contact form ##')
        response = self.contact('', 'nanoha@microsoft.com', '', '') # empty name, empty email, empty title, empty enquiry
        self.assertIn(b'Missing compulsory fields', response.data)

    # Testing contact form with email, title and enquiry
    def test_email_title_enquiry_contact_form(self):
        print('\n## Testing Submitting with empty contact form ##')
        response = self.contact('', 'nanoha@microsoft.com', 'Hey', 'I have something to say.') # empty name, empty email, empty title, empty enquiry
        self.assertIn(b'Enquiry sent! YAY! Y^_^Y', response.data)

    # Testing contact form with all fields filled
    def test_all_filled_contact_form(self):
        print('\n## Testing Submitting with empty contact form ##')
        response = self.contact('Nanoha', 'nanoha@microsoft.com', 'Hey', 'I have something to say.') # empty name, empty email, empty title, empty enquiry
        self.assertIn(b'Enquiry sent! YAY! Y^_^Y', response.data)

    def contact(self, name, email, title, enquiry):
        return self.client.post('/contact', data=dict(
            name=name,
            email=email,
            title=title,
            enquiry=enquiry
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
