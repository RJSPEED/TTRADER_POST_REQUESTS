import sqlite3
import os
import unittest
from app.orm import ORM
from app import Account, Position, Trade
from data.seed import seed
from data.schema import schema

DIR = os.path.dirname(__file__)
DBFILENAME = "_test.db"
DBPATH = os.path.join(DIR, DBFILENAME)

""" setting ORM.dbpath changes the db for all classes inheriting from it """
ORM.dbpath = DBPATH

class TestAccount(unittest.TestCase):
    def setUp(self):
        """ the setup method must be called setup """
        schema(DBPATH)
        seed(DBPATH)

    # def tearDown(self):
    #     """ the tear down method must be called tearDown """
    #     os.remove(DBPATH)
    
    def test_key_creation(self):
        #Create new account record incl. api_key and save to DB
        new_user = Account(username="test_user")
        new_user.set_password("test_password")
        new_user.create_api_key()
        new_user.save()
        
        #Retrieve new account record and evaluate api_key pop'd
        pk = new_user.pk
        same_user = Account.one_from_pk(pk)
        self.assertEqual(len(same_user.api_key), 15, "api key populated")

    