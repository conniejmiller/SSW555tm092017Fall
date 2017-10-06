import unittest
import project


TEST_FILE_NAME = 'data/testing.ged'
words = project.process_file(TEST_FILE_NAME)
individuals, families = project.process_words(words)


class TestProject(unittest.TestCase):

    def test_empty(self):
        """ Testing the process_words function """
        word_matrix = [[]]
        self.assertEqual(project.process_words(word_matrix), ([], []))

    def test_date_compare(self):
        """ Testing the date_compare function  """
        self.assertEqual(project.date_compare('10 SEP 2017'), True)
        self.assertTrue(project.date_compare('10 SEP 2017'))
        self.assertEqual(project.date_compare('10 SEP 2018'), False)
        self.assertEqual(project.date_compare('20 SEP 2017'), True)
        self.assertNotEqual(project.date_compare('10 SEP 2017'), False)
        self.assertNotEqual(project.date_compare('10 SEP 2018'), True)

    def test_is_deceased(self):
        """ Testing the is_deceased function  """
        self.assertEqual(project.is_deceased(''), False)
        self.assertEqual(project.is_deceased('11 SEP 1998'), True)
        self.assertEqual(project.is_deceased('18 MAR 2007'), True)
        self.assertFalse(project.is_deceased(''), True)
        self.assertTrue(project.is_deceased('18 MAR 2007'), True)

    def test_life_duration(self):
        """ Testing if life duration is less than 150 years"""
        self.assertTrue(project.valid_lifetime('01 JAN 1980', '01 JAN 2020'))
        self.assertTrue(project.valid_lifetime('01 JAN 1985', '01 JAN 2020'))
        self.assertTrue(project.valid_lifetime('01 JAN 1000', '01 JAN 1149'))
        self.assertFalse(project.valid_lifetime('01 JAN 1000', '01 JAN 1150'))
        self.assertFalse(project.valid_lifetime('01 JAN 1500', '01 JAN 2520'))
        self.assertFalse(project.valid_lifetime('01 JAN 1000', '01 JAN 2220'))

    def test_calculate_years(self):
        """ Testing the calculate_years function  """
        self.assertEqual(project.calculate_years('09 FEB 1962',
                                                 '11 SEP 2017'), 55)
        self.assertEqual(project.calculate_years('10 SEP 1969',
                                                 '11 SEP 1999'), 30)
        self.assertEqual(project.calculate_years('23 OCT 1989',
                                                 '11 SEP 2017'), 27)

    def test_valid_lifetime(self):
        """ Testing the valid_lifetime function  """
        self.assertEqual(project.valid_lifetime('11 SEP 1998',
                                                '11 SEP 1999'), True)
        self.assertEqual(project.valid_lifetime('11 SEP 1898',
                                                '11 SEP 1999'), True)
        self.assertEqual(project.valid_lifetime('11 SEP 1798',
                                                '11 SEP 1999'), False)

    def test_get_age(self):
        """ Testing the get_age function  """
        self.assertEqual(project.get_age(individuals, '@I1@'), 117)
        self.assertEqual(project.get_age(individuals, '@I3@'), 78)
        self.assertEqual(project.get_age(individuals, '@I4@'), 80)

    def test_validate_birth_dates(self):
        """ Testing the validate_indi_dates function """
        self.assertEqual(project.validate_birth_dates(individuals[0]), 'none')
        self.assertEqual(project.validate_birth_dates(individuals[1]), 'US42')
        self.assertEqual(project.validate_birth_dates(individuals[5]), 'US01')

    def test_get_name_id(self):
        """ Testing the get_name_id function """
        self.assertEqual(project.get_name_id(individuals[0]),
                         'Bob /Jones/ (@I1@)')
        self.assertEqual(project.get_name_id(individuals[1]),
                         'Mary /Smith/ (@I2@)')
        self.assertEqual(project.get_name_id(individuals[2]),
                         'Thelma Lucella /Philbrook/ (@I3@)')

    def test_get_name_id_list(self):
        """ Testing the get_name_id function """
        self.assertEqual(project.get_name_id_list(individuals, '@I1@'),
                         'Bob /Jones/ (@I1@)')
        self.assertEqual(project.get_name_id_list(individuals, '@I2@'),
                         'Mary /Smith/ (@I2@)')
        self.assertEqual(project.get_name_id_list(individuals, '@I3@'),
                         'Thelma Lucella /Philbrook/ (@I3@)')

    def test_valid_month(self):
        """ Testing is month is valid """
        self.assertTrue(project.valid_month('01 JAN 1980'))
        self.assertTrue(project.valid_month('01 FEB 1980'))
        self.assertTrue(project.valid_month('01 MAR 1980'))
        self.assertFalse(project.valid_month('01 JAM 1980'))
        self.assertFalse(project.valid_month('01 ABC 1980'))

    def test_validate_genders(self):
        """ validate_genders(families, individuals):
            if husband and wife genders accurate, return True
        """
        self.assertFalse(project.validate_genders(families, individuals))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
