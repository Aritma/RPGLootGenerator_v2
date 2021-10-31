import unittest

from sqlalchemy import inspect
from database.db_worker import DBWorker


class DBWorkerTest(unittest.TestCase):

    def setUp(self):
        self.db_worker = DBWorker()
        self.inspector = inspect(self.db_worker.engine)

    def test_db_has_table(self):
        self.assertTrue(self.inspector.has_table('items'))
        self.assertTrue(self.inspector.has_table('tags'))

    def test_inserts_value_into_items(self):
        self.db_worker.register_item(name='test', source='test', description='test', tags=['test'])
        self.assertEqual(
            self.db_worker.session.execute("SELECT * FROM items").fetchall(),
            [(1, 'test', 'test', 'test')]
        )
        self.assertEqual(
            self.db_worker.session.execute("SELECT * FROM tags").fetchall(),
            [(1, 'test')]
        )
