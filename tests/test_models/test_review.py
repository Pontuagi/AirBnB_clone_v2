#!/usr/bin/python3

""" Test Module for review.py """

from tests.test_models.test_base_model import test_basemodel
from models.review import Review
from models.place import Place
from models.user import User


class test_review(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.text), str)

    def test_place_relationship(self):
        """Test the relationship between Review and Place"""
        place = Place(name="Test Place")
        review = Review(text="Test review", place=place)
        self.assertEqual(review.place, place)

    def test_user_relationship(self):
        """Test the relationship between Review and User"""
        user = User(email="test@example.com", password="password")
        review = Review(text="Test review", user=user)
        self.assertEqual(review.user, user)
