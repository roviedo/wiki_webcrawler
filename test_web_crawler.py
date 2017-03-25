import unittest
from web_crawler import (
    update_path_length_distribution,
    parenthesis_match,
    output_metrics
)


class TestStringMethods(unittest.TestCase):

    def test_update_path_length_distribution(self):
        path_length_distribution = {}
        path = 9
        update_path_length_distribution(path_length_distribution, path)
        self.assertEqual(path_length_distribution, {'9': 1})

    def test_parenthesis_match_append(self):
        string = "was a  ( Sevillian painter. Born in 1929, she moved " \
                 "to Madrid in 1958 and lived there until she died in 2012."
        parenthesis_stack = []
        parenthesis_match(string, parenthesis_stack)
        self.assertEqual(parenthesis_stack, ['('])

    def test_parenthesis_match_pop(self):
        string = "was a Sevillian painter.) Born in 1929, she moved " \
                 "to Madrid in 1958 and lived there until she died in 2012."
        parenthesis_stack = ['(']
        parenthesis_match(string, parenthesis_stack)
        self.assertEqual(parenthesis_stack, [])

    def test_output_metrics(self):
        path_length_distribution = {'None': 1, '12': 2, '10': 2}
        pages_amount = 5
        (pages_that_lead_to_phi, average, path_length_distribution) = \
                 output_metrics(path_length_distribution, pages_amount)
        self.assertEqual(pages_that_lead_to_phi, 4)
        self.assertEqual(average, 11.0)


if __name__ == '__main__':
    unittest.main()
