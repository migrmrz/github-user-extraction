import unittest
import sqlite3
from ..code.seed import get_user_data_from_github, \
                        convert_user_data, \
                        process_user_data_to_db
from ..code.db import GithubDatabase


class TestSeedScript(unittest.TestCase):

    def test_get_user_data_from_github_type(self):
        users_data = get_user_data_from_github()
        self.assertIsInstance(users_data, list)
        for user_data in users_data:
            self.assertIsInstance(user_data, dict)

    def test_get_user_data_from_github_total_results(self):
        users_data = get_user_data_from_github()
        self.assertEqual(len(users_data), 150)

    def test_get_user_data_from_github_total_custom_results(self):
        total = 200
        users_data = get_user_data_from_github(total)
        self.assertEqual(len(users_data), total)

    def test_convert_user_data_type(self):
        users_data = get_user_data_from_github()
        users_rows = convert_user_data(users_data)
        self.assertIsInstance(users_rows, list)
        for user_row in users_rows:
            self.assertIsInstance(user_row, tuple)

    def test_create_db_connection(self):
        db = "../db/test_github.db"
        gdb = GithubDatabase(db)
        self.assertIsInstance(gdb.conn, sqlite3.Connection)
        gdb.close()

    def test_process_user_data_to_db(self):
        users_data = get_user_data_from_github()
        users_rows = convert_user_data(users_data)
        db = "../db/test_github.db"
        inserted_rows = process_user_data_to_db(users_rows, db)
        self.assertEqual(int(inserted_rows), 150)

    def test_process_user_data_to_db_many_records(self):
        total = 5000
        users_data = get_user_data_from_github(total)
        users_rows = convert_user_data(users_data)
        db = "../db/test_github.db"
        inserted_rows = process_user_data_to_db(users_rows, db)
        self.assertEqual(int(inserted_rows), total)
