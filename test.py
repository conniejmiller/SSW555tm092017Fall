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

    def test_get_age(self):
        """ Testing the get_age function  """
        self.assertEqual(project.get_age(individuals, '@I1@'), 117)
        self.assertEqual(project.get_age(individuals, '@I3@'), 78)
        self.assertEqual(project.get_age(individuals, '@I4@'), 80)

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

    def test_valid_lifetime(self):
        """ valid_lifetime(birth, death) 
            if years is below 150,
            return True
        """ 
        birth = '30 APR 1989'
        death = '30 APR 1960'
        invalid_birth = '30 APR 1850'
        invalid_death = '30 APR 2017'
        self.assertTrue(project.valid_lifetime(birth, death))
        self.assertFalse(project.valid_lifetime(invalid_birth, invalid_death))

    def test_is_below150_years(self):
        """ is_below150_years(life_years)
            if years is below 150,
            return True 
        """
        self.assertTrue(project.is_below150_years(90))
        self.assertTrue(project.is_below150_years(9))
        self.assertFalse(project.is_below150_years(160))



if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
