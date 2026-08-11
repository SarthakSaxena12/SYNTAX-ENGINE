import unittest
import sys
import os

# Allows the test to find parser.py and rules.py in the parent folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parser import parse

class TestHeadings(unittest.TestCase):

    def test_h1(self):
        self.assertEqual(parse("# Hello World"), "<h1>Hello World</h1>")

    def test_h2(self):
        self.assertEqual(parse("## Subtitle"), "<h2>Subtitle</h2>")

    def test_h6(self):
        self.assertEqual(parse("###### Smallest"), "<h6>Smallest</h6>")

    def test_no_header(self):
        self.assertEqual(parse("Just plain text"), "<p>Just plain text</p>")

    def test_seven_hashes_is_not_a_header(self):
        # CommonMark rule: more than 6 #'s is not a valid heading
        self.assertEqual(parse("####### Too many"), "<p>####### Too many</p>")

    def test_hash_with_no_space_is_not_a_header(self):
        # CommonMark rule: needs a space after the #'s
        self.assertEqual(parse("#NoSpace"), "<p>#NoSpace</p>")

if __name__ == '__main__':
    unittest.main()