import unittest
from project import *
from validate import *
from display import *
from helpers import *

TEST_FILE_NAME = 'data/testing.ged'
gedcom = Gedcom(TEST_FILE_NAME)
individuals = gedcom.individual
families = gedcom.family


class TestProject(unittest.TestCase):

    def test_date_compare(self):
        """ Testing the date_compare function  """
        self.assertEqual(date_compare('10 SEP 2017',''), True)
        self.assertTrue(date_compare('10 SEP 2017',''))
        self.assertEqual(date_compare('10 SEP 2018','10 SEP 2017'), False)
        self.assertEqual(date_compare('20 SEP 2017','10 SEP 2018'), True)

    def test_is_deceased(self):
        """ Testing the is_deceased function  """
        self.assertEqual(is_deceased(''), False)
        self.assertEqual(is_deceased('11 SEP 1998'), True)
        self.assertEqual(is_deceased('18 MAR 2007'), True)
        self.assertFalse(is_deceased(''), True)
        self.assertTrue(is_deceased('18 MAR 2007'), True)

    def test_life_duration(self):
        """ Testing if life duration is less than 150 years"""
        self.assertTrue(valid_lifetime('01 JAN 1980', '01 JAN 2020'))
        self.assertTrue(valid_lifetime('01 JAN 1985', '01 JAN 2020'))
        self.assertTrue(valid_lifetime('01 JAN 1000', '01 JAN 1149'))
        self.assertFalse(valid_lifetime('01 JAN 1000', '01 JAN 1150'))
        self.assertFalse(valid_lifetime('01 JAN 1500', '01 JAN 2520'))
        self.assertFalse(valid_lifetime('01 JAN 1000', '01 JAN 2220'))

    def test_get_age(self):
        """ Testing the get_age function  """
        self.assertEqual(get_age(individuals, '@I1@'), 117)
        self.assertEqual(get_age(individuals, '@I3@'), 78)
        self.assertEqual(get_age(individuals, '@I4@'), 80)

    def test_valid_month(self):
        """ Testing is month is valid """
        self.assertTrue(valid_month('01 JAN 1980'))
        self.assertTrue(valid_month('01 FEB 1980'))
        self.assertTrue(valid_month('01 MAR 1980'))
        self.assertFalse(valid_month('01 JAM 1980'))
        self.assertFalse(valid_month('01 ABC 1980'))

    def test_validate_genders(self):
        """ validate_genders(families, individuals):
            if husband and wife genders accurate, return True
        """
        self.assertFalse(validate_genders(families, individuals))

    def test_calculate_years(self):
        """ Testing the calculate_years function  """
        self.assertEqual(calculate_years('09 FEB 1962', '11 SEP 2017'), 55)
        self.assertEqual(calculate_years('10 SEP 1969', '11 SEP 1999'), 30)
        self.assertEqual(calculate_years('23 OCT 1989', '11 SEP 2017'), 27)

    def test_valid_lifetime(self):
        """ Testing the valid_lifetime function  """
        self.assertEqual(valid_lifetime('11 SEP 1998', '11 SEP 1999'), True)
        self.assertEqual(valid_lifetime('11 SEP 1898', '11 SEP 1999'), True)
        self.assertEqual(valid_lifetime('11 SEP 1798', '11 SEP 1999'), False)

    def test_get_name(self):
        """ Testing the get_age function  """
        self.assertEqual(get_name(individuals, '@I1@'), 'Bob /Jones/')
        self.assertEqual(get_name(individuals, '@I2@'), 'Mary /Smith/')

    def test_get_birth(self):
        """ Testing the get_age function  """
        self.assertEqual(get_birth(individuals, '@I1@'), '1 JAN 1900')
        self.assertEqual(get_birth(individuals, '@I3@'), '18 FEB 1939')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
