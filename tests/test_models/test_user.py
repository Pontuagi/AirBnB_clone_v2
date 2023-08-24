#!/usr/bin/python3

""" Test cases for Users module """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from models.place import Place
from models.review import Review


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)

    def test_places_relationship(self):
        """Test the relationship between User and Place"""
        user = User(email="test@example.com", password="password")
        place1 = Place(name="Place 1", user=user)
        place2 = Place(name="Place 2", user=user)
        self.assertIn(place1, user.places)
        self.assertIn(place2, user.places)

    def test_reviews_relationship(self):
        """Test the relationship between User and Review"""
        user = User(email="test@example.com", password="password")
        review1 = Review(text="Review 1", user=user)
        review2 = Review(text="Review 2", user=user)
        self.assertIn(review1, user.reviews)
        self.assertIn(review2, user.reviews)
