import unittest
import os

from .settings import *
from .context import csvparse

class TestCSVParse(unittest.TestCase):
    
    def setUp(self):
        self.db_name = DB_NAME
        self.table_name = DB_TABLE
        self.client = csvparse.CSVParse(self.db_name, self.table_name)
        dirname = os.path.dirname(__file__)
        self.sample_dir = os.path.join(dirname, 'sample')

    def test_project_sample_one_processed(self):
        sample1_rows = 171
        
        success, inserted, total_rows = self.client.process_csv(self.sample_dir + "/sample1.csv")
        self.assertTrue(success)
        self.assertEqual(sample1_rows, inserted)
        self.assertEqual(sample1_rows, total_rows)
        self.assertTrue(os.path.isfile(self.db_name))

    def test_project_sample_two_processed(self):
        sample2_rows = 141
        
        success, inserted, total_rows = self.client.process_csv(self.sample_dir + "/sample2.csv")
        self.assertTrue(success)
        self.assertEqual(sample2_rows, inserted)
        self.assertEqual(sample2_rows, total_rows)
        self.assertTrue(os.path.isfile(self.db_name))

if __name__ == '__main__':
    unittest.main()