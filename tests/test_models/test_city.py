#!/usr/bin/python3

""" Test module for City"""

from tests.test_models.test_base_model import test_basemodel
from models.city import City
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.place import Place  # Import Place
from models.base_model import Base  # Import Base


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def setUp(self):
        """Set up the test environment"""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Tear down the test environment"""
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_relationship(self):
        """Test the relationship between City and Place"""
        city = City(name="Example City", state_id="state-123")
        place = Place(name="Example Place", city=city)
        self.session.add(city)
        self.session.add(place)
        self.session.commit()

        self.assertEqual(city.places[0], place)
        self.assertEqual(place.city, city)
