import unittest
import json
from smtpapi import SMTPAPIHeader


class TestSMTPAPI(unittest.TestCase):

    def setUp(self):
        self.validHeader = json.loads('''{"to":["test@email.com",
        "test2@email.com", "test3@email.com"],
        "sub":{"subKey":["subValue"]},
        "section":{"testSection":"sectionValue"},
        "category":["testCategory"],
        "unique_args":{"testUnique":"uniqueValue"},
        "filters":{"testFilter":{"settings":{"filter":"filterValue"}}}}''')

        self.dropsHeader = json.loads('''{
        "sub":{"subKey":["subValue"]},
        "unique_args":{"testUnique":"uniqueValue"},
        "filters":{"testFilter":{"settings":{"filter":"filterValue"}}}}''')

    def test_add(self):
        header = SMTPAPIHeader()
        header.add_to('test@email.com')
        header.add_to(['test2@email.com', 'test3@email.com'])
        header.add_substitution('subKey', 'subValue')
        header.add_section('testSection', 'sectionValue')
        header.add_category('testCategory')
        header.add_unique_arg('testUnique', 'uniqueValue')
        header.add_filter('testFilter', 'filter', 'filterValue')
        self.assertEqual(self.validHeader, json.loads(header.json_string()))

    def test_set(self):
        header = SMTPAPIHeader()
        header.set_tos(["test@email.com", "test2@email.com", "test3@email.com"])
        header.set_substitutions(json.loads('{"subKey":["subValue"]}'))
        header.set_sections(json.loads('{"testSection":"sectionValue"}'))
        header.set_categories(["testCategory"])
        header.set_unique_args(json.loads('{"testUnique":"uniqueValue"}'))
        header.add_filter('testFilter', 'filter', 'filterValue')
        self.assertEqual(self.validHeader, json.loads(header.json_string()))

    def test_drop_empty(self):
        header = SMTPAPIHeader()
        header.set_tos([])
        header.set_substitutions(json.loads('{"subKey":["subValue"]}'))
        header.set_sections(json.loads('{}'))
        header.set_categories([])
        header.set_unique_args(json.loads('{"testUnique":"uniqueValue"}'))
        header.add_filter('testFilter', 'filter', 'filterValue')
        self.assertEqual(self.dropsHeader, json.loads(header.json_string()))


if __name__ == '__main__':
    unittest.main()
