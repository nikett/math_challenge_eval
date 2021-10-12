import unittest

from src.utils import *


class UtilsTestCase(unittest.TestCase):
    def test_abbreviate(self):
        self.assertEqual(abbreviate_lname("Tandon"), "T.")
        self.assertEqual(abbreviate_lname("tandon"), "T.")
        self.assertEqual(abbreviate_lname("t"), "T.")
        self.assertEqual(abbreviate_lname(""), "")


if __name__ == '__main__':
    unittest.main()
