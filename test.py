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

	def test_feedback(self):
		with self.client as c:
			with c.session_transaction() as session:
				session['logged_in'] = True
				session['email'] = 'singarisathwik007@gmail.com'
				session['firstname'] = 'Sathwik'
				session['lastname'] = 'Singari'
				print('\n## Testing feedback page ##')

		response = self.client.post('/feedback', data=dict(
			username="sam",
			email="example@gmail.com",
			subject="test message",
			message="Good!"
			), follow_redirects=True)
		
		self.assertIn(b'Thank', response.data)




if __name__ == '__main__':
    unittest.main()
