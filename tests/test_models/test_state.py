#!/usr/bin/python3

""" Test for State.py Module"""

from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.city import City


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_cities_relationship(self):
        """Test the relationship between State and City"""
        state = State(name="Test State")
        city1 = City(name="City 1", state=state)
        city2 = City(name="City 2", state=state)
        self.assertIn(city1, state.cities)
        self.assertIn(city2, state.cities)
