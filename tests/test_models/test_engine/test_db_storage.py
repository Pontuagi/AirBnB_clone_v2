#!/usr/bin/python3
import os
import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime

@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "DBStorage only")

class test_DBStorage(unittest.TestCase):
    """Tests for the DB storage class """

    def setUp(self):
        """Set up test environment"""
        self.db = DBStorage()

    def tearDown(self):
        """Removes stoprage file at the end of tests"""
        self.db.close()

    def test_all(self):
        """Tests all methods of DBStorage"""
        objs = self.db.all()
        self.assertIsInstance(objs, dict)

    def test_all_cls(self):
        """Tests all methods with class filter"""
        objs = self.db.all(BaseModel)
        self.assertIsInstance(objs, dict)

    def test_new(self):
        """Tests new method of DBStorage"""
        new_obj = BaseModel()
        self.db.new(new_obj)
        obj_id = new_obj.id
        key = "BaseModel." + obj_id
        self.assertIn(key, self.db.all())

    def test_save(self):
        """Tests save method of DB storage"""
        new_obj = BaseModel()
        self.db.new(new_obj)
        self.db.save()
        obj_id = new_obj.id
        key = "BaseModel." + obj_id
        self.assertIn(key, self.db.all())

    def test_delete(self):
        """Tests the delete method of DBStorage"""
        new_obj = BaseModel()
        self.db.new(new_obj)
        self.db.save()
        obj_id = new_obj.id
        key = "BaseModel." + obj_id
        self.assertIn(key, self.db.all())
        self.db.delete(new_obj)
        self.assertNotIn(key, self.db.all())

    def test_reload(self):
        """Tests reload method of DBStorage"""
        self.db.reload()
        self.assertIsInstance(self.db._DBStorage__session, Session)

    def test_close(self):
        """Tests close method of DBStorage"""
        self.db.close()
        self.assertIsNone(self.db._DBStorage__session)


if __name__ == "__main__":
    unittest.main()
