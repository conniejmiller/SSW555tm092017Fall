from validate import validate_dates, validate_genders, validate_males
from validate import validate_marriages, validate_ids, validate_name_birth
from validate import validate_divorces, validate_siblings
from display import print_table
from helpers import list_deceased, get_recent_deaths, get_recent_births2
from helpers import get_living_married, list_living_single, create_family_dict, process_partial_dates
from pprint import pprint
from helpers import get_living_married, list_living_single, sort_siblings
from helpers import list_large_age_differences

FILE_NAME = 'data/baseline_input.ged'
TEST_FILE_NAME = 'data/testing.ged'


class Gedcom():
    """
    The loader and handler for GEDCOM files
    """
    def __init__(self, file_name):
        try:
            self.words = self._process_file(file_name)
            self.individual, self.family = self._process_words(self.words)
        except:
            print("Unable to process input file")
            self.words = None
            self.individual = None
            self.family = None

    def _process_words(self, wordMatrix):
        """ Process rows in the matrix """
        this_type = 'new'
        this_tag = 'new'
        individual = []
        family = []
        indi_dict = {}
        fam_dict = {}

        for words in wordMatrix:
            if len(words) >= 2:
                tag = words[1]
                other_stuff = words[2:]

                if len(words) == 3 and words[2] in ("INDI", "FAM"):
                    # print lastline
                    if this_type == 'INDI':
                        individual.append(indi_dict)
                    elif this_type == 'FAM':
                        family.append(fam_dict)

                    if words[2] == "INDI":
                        indi_dict = {"ID": tag,
                                     "NAME": '',
                                     "SEX": '',
                                     "BIRT": '',
                                     "DEAT": ''}
                        this_type = 'INDI'
                    else:
                        fam_dict = {"ID": tag,
                                    "MARR": '',
                                    "HUSB": '',
                                    "WIFE": '',
                                    "CHIL": [],
                                    "DIV": ''}
                        this_type = 'FAM'

                elif tag in ("NAME", "SEX"):
                    indi_dict[tag] = " ".join(other_stuff)

                elif tag in ("BIRT", "DEAT", "MARR", "DIV"):
                    # savethis tag so we can write it after the next row
                    this_tag = tag

                elif tag in ("DATE"):
                    if this_type == 'INDI':
                        indi_dict[this_tag] = " ".join(other_stuff)
                    elif this_type == 'FAM':
                        fam_dict[this_tag] = " ".join(other_stuff)
                    this_tag = 'new'

                elif tag in ("HUSB", "WIFE"):
                    fam_dict[tag] = " ".join(other_stuff)

                elif tag == "CHIL":
                    fam_dict[tag].append(words[2])

        sort_siblings(fam_dict["CHIL"], individual)

        # now print the last one
        if this_type == 'INDI':
            individual.append(indi_dict)
        elif this_type == 'FAM':
            family.append(fam_dict)
        
        for row in family:
            if row['MARR'] or row['DIV']:  
                row['MARR'] = process_partial_dates(row['MARR'])
                row['DIV'] = process_partial_dates(row['DIV'])

        for row in individual:
            if row['BIRT'] or row['DEAT']:  
                row['BIRT'] = process_partial_dates(row['BIRT'])
                row['DEAT'] = process_partial_dates(row['DEAT'])

        return individual, family

    def _process_file(self, filename):
        """  Process the file """
        words = []

        # read the file and process the rows
        with open(filename) as in_file:
            for line in in_file:
                words.append(line.split())

        return words

    def display(self):
        """Display the contents of the GEDCOM file"""
        print_table(self.individual, self.family)
        list_deceased(self.individual)
        get_recent_deaths(self.individual)
        get_recent_births(self.individual)
        get_living_married(self.family, self.individual)
        list_living_single(self.individual, self.family)
        create_family_dict(self.family, self.individual)
        list_large_age_differences(self.family, self.individual)

    def validate(self):
        """Validate the contents of the GEDCOM file"""
        validate_dates(self.family, self.individual)
        validate_genders(self.family, self.individual)
        validate_males(self.family, self.individual)
        validate_divorces(self.family, self.individual)
        validate_marriages(self.family, self.individual)
        validate_ids(self.family, self.individual)
        validate_name_birth(self.individual)
        validate_siblings(self.family)


def main():
    """ Main processing function
    """
    gedcom = Gedcom(FILE_NAME)
    gedcom.display()
    gedcom.validate()

if __name__ == '__main__':
    main()
