#!/usr/bin/python3
"""
This module contains the various test cases for the base module
"""


import datetime
from models import base_model
from models.base_model import BaseModel
import os
from time import sleep
import unittest


class BaseModelTest(unittest.TestCase):
    """
    This class contains various test cases to test the BaseModel class
    """

    def setUp(self):
        """
        Make an instance of the base model class to be used for testing
        out the class
        """
        self.bm = BaseModel()
        try:
            os.rename("file.json", "tmp")
        except Exception:
            pass

    def test_mod_doc(self):
        self.assertNotEqual(len(base_model.__doc__.split()), 0)

    def test_base_doc(self):
        self.assertNotEqual(len(self.bm.__doc__.split()), 0)

    def test_base_save(self):
        self.assertNotEqual(len(self.bm.save.__doc__.split()), 0)

    def test_base_to_dict(self):
        test_dict = self.bm.to_dict()
        self.assertNotEqual(len(self.bm.to_dict.__doc__.split()), 0)
        self.assertIsInstance(test_dict, dict)
        self.assertIn("__class__", test_dict)
        self.assertIsInstance(test_dict["created_at"], str)
        self.assertIsInstance(test_dict["updated_at"], str)

    def test_base_str(self):
        self.assertNotEqual(len(str(self.bm)), 0)
        self.assertRegex(str(self.bm), r"^\[[a-z-A-Z]+\] \(.+\) {.+}$")

    def test_base_init_r1(self):
        self.assertTrue(BaseModel())

    def test_base_init_r2(self):
        dic = self.bm.to_dict()
        b = BaseModel(**dic)
        self.assertTrue(b != self.bm)

    def test_base_init_r3(self):
        b = BaseModel(5)
        self.assertTrue(BaseModel(5))

    def test_instance(self):
        """Test if it produces an instance"""
        b = BaseModel()
        self.assertTrue(isinstance(b, BaseModel))

    def test_uuid(self):
        """test uid"""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertTrue(isinstance(b1.id, str))
        self.assertFalse(b1.id == b2.id)

    def test_created_at(self):
        """tests createdat and updated_at"""
        b = BaseModel()
        self.assertIsInstance(b.created_at, datetime.datetime)
        self.assertIsInstance(b.updated_at, datetime.datetime)

    def test_save(self):
        """tests the save function"""
        b = BaseModel()
        init = b.updated_at
        sleep(1)
        b.save()
        self.assertTrue(os.path.isfile("file.json"))
        self.assertNotEqual(init, b.updated_at)
        with self.assertRaises(TypeError):
            b.save(None)

    def tearDown(self):
        try:
            os.remove("file.json")
        except Exception:
            pass
        try:
            os.rename("tmp", "file.json")
        except Exception:
            pass
