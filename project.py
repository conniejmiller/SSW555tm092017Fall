from operator import itemgetter
from prettytable import PrettyTable
from datetime import datetime
from math import floor

FILE_NAME = 'data/baseline_input.ged'
TEST_FILE_NAME = 'data/testing.ged'


def valid_tag(level, tag):
    """ Defines a dict of valid tags at each level,
        checks for a valid combination, and returns "Y" or "N"
    """
    valid_tags = {"0": ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
                  "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS",
                        "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                  "2": ["DATE"]}

    return "Y" if level in valid_tags and tag in valid_tags[level] else "N"


def print_line(level, tag, args):
    """ Print the formatted line of level, tag, and arguments """
    print("<-- %s|%s|%s|%s" % (level, tag, valid_tag(level, tag), args))


def getname(list, id):
    """ Get the name for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"


def process_words(wordMatrix):
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

    # now print the last one
    if this_type == 'INDI':
        individual.append(indi_dict)
    elif this_type == 'FAM':
        family.append(fam_dict)

    return individual, family


def print_indi(individual):
    """ Print individuals """
    for row in sorted(individual, key=itemgetter("ID")):
        print(row["ID"] + " : " + row["NAME"])


def print_fam(individual, family):
    """ Print families """
    for row in sorted(family, key=itemgetter("ID")):
        print(row["ID"] + " : " +
              row["HUSB"] + ":" + getname(individual, row["HUSB"]) +
              " and " +
              row["WIFE"] + ":" + getname(individual, row["WIFE"]))


def print_table(individual, family):
    """ Print table of individuals and families """
    individuals = PrettyTable(["ID",
                               "NAME",
                               "GENDER",
                               "BIRTHDAY",
                               "DEATH"])
    # One space between column edges and contents (default)
    individuals.padding_width = 1
    individuals.align["NAME"] = "l"  # Left align names
    for row in sorted(individual, key=itemgetter("ID")):
        individuals.add_row([row["ID"],
                             row["NAME"],
                             row["SEX"],
                             row["BIRT"],
                             row["DEAT"]])
    print(individuals)

    families = PrettyTable(["ID",
                            "MARRIED",
                            "DIVORCED",
                            "HUSBAND",
                            "WIFE",
                            "CHILDREN"])
    # One space between column edges and contents (default)
    families.padding_width = 1
    families.align["HUSBAND"] = "1"
    families.align["WIFE"] = "1"

    for row in sorted(family, key=itemgetter("ID")):
        families.add_row([row["ID"],
                          row["MARR"],
                          row["DIV"],
                          row["HUSB"] + ":" + getname(individual, row["HUSB"]),
                          row["WIFE"] + ":" + getname(individual, row["WIFE"]),
                          row["CHIL"]])

    print(families)


def process_file(filename):
    """  Process the file """
    words = []

    # read the file and process the rows
    with open(filename) as in_file:
        for line in in_file:
            words.append(line.split())

    return words


def is_deceased(row_death):
    """ Check if an individual is dea and return a Boolean val """
    try:
        row_death = str(row_death)
        if not row_death:
            return False
        else:
            return True
    except ValueError:
        print('Invalid type.')


def list_deceased(indi_list):
    """ This function loops through the individual list and prints
        names of deceased people
    """
    for row in indi_list:
        if is_deceased(row["DEAT"]):
            print('Deceased: {0}, {1}'.format(row["NAME"], row['DEAT']))


def valid_month(date):
    """ This function determines if a given month is valid """
    if date != '':
        month = date.split()[1]
    else:
        return True

    valid_months = ["JAN", "FEB", "MAR", "APR",
                    "MAY", "JUN", "JUL", "AUG",
                    "SEP", "OCT", "NOV", "DEC"]

    if month in valid_months:
        return True
    else:
        return False


def date_compare(a):
    """ This routine compares a date in the Exact format to the current date
        and returns true if it is prior to today
        otherwise, returns false
    """
    # print (datetime.now())
    new_date = datetime.strptime(a, '%d %b %Y').date()
    # print(new_date)

    if new_date < datetime.now().date():
        return True
    else:
        return False


def valid_lifetime(birth, death):
    """ This routine validates the duration of life """
    if birth != '' and death != '':
        death_date = datetime.strptime(death, '%d %b %Y').date()
        birth_date = datetime.strptime(birth, '%d %b %Y').date()

        life_years = (death_date - birth_date).days / 365
        if life_years < 150:
            return True
        else:
            return False


def get_age(list, id):
    """ This returns the the age of a given individual """
    for row in list:
        if row["ID"] == id:
            birth_date = row["BIRT"]
            if valid_month(birth_date):
                birth_date = datetime.strptime(birth_date, '%d %b %Y').date()
                today = datetime.now().date()
                age = (today - birth_date).days / 365
                return floor(age)
            return -1
    return -1


def validate_dates(indi_list, fam_list):
    for row in indi_list:
        birth_date = row["BIRT"]
        death_date = row["DEAT"]

        if not valid_month(birth_date):
            print('Error US42: Invalid birth month for ' +
                  row["NAME"] + ' (' + row["ID"] + ') ')
        elif not date_compare(birth_date):
            print('Error US01: Birth date of ' +
                  row["NAME"] + ' (' + row["ID"] + ') ' +
                  'occurs after the current date.')
        # if death date was defined
        if not valid_month(death_date):
            print('Error US42: Invalid death month for ' +
                  row["NAME"] + ' (' + row["ID"] + ') ')
        elif death_date != '' and not date_compare(row["DEAT"]):
            print('Error US01: Death date of ' +
                  row["NAME"] + ' (' + row["ID"] + ') ' +
                  'occurs after the current date.')

            if not valid_lifetime(birth_date, death_date):
                print('Error US07: Life duration of ' +
                      row["NAME"] + ' (' + row["ID"] + ') ' +
                      'is greater than 150 years.')

    for row in fam_list:
        # if marriage date was not defined - anomaly
        if row["MARR"] == '':
            print('Anomaly: No marriage date exists for family (' +
                  row["ID"] + ').')
        elif not valid_month(row["MARR"]):
            print('Error US42: Invalid marriage month for ' +
                  getname(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  getname(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ')')
        elif not date_compare(row["MARR"]):
            print('Error US01: Marriage date of ' +
                  getname(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  getname(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ') occurs after the current date.')

        # if divorce date was defined
        if not valid_month(row["DIV"]):
            print('Error US42: Invalid divorce month for ' +
                  getname(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  getname(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ')')
        elif row["DIV"] != '' and not date_compare(row["DIV"]):
            print('Error US01: Divorce date of ' +
                  getname(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  getname(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ') occurs after the current date.')

        # if children exist, check ages of parents at birth
        if row["CHIL"] != '':
            # get current age of parents
            dad_age = get_age(indi_list, row["HUSB"])
            mom_age = get_age(indi_list, row["WIFE"])
            for child in row["CHIL"]:
                child_age = get_age(indi_list, child)
                if (dad_age - child_age) >= 80:
                    print('Anomaly US12: Father ' +
                          getname(indi_list, row["HUSB"]) +
                          ' (' + row["HUSB"] +
                          ') was older than 80 when ' +
                          getname(indi_list, child) + ' (' + child +
                          ') was born.')
                elif (mom_age - child_age) >= 60:
                    print('Anomaly US12: Mother ' +
                          getname(indi_list, row["WIFE"]) +
                          ' (' + row["WIFE"] +
                          ') was older than 60 when ' +
                          getname(indi_list, child) + ' (' + child +
                          ') was born.')


def main():
    """ Main processing function. calls process_file(), print_indi() print_fam()
        and print_table()
    """
    words = process_file(FILE_NAME)
    # To be used as a test input
    # words = process_file(TEST_FILE_NAME)

    individual, family = process_words(words)

    print_table(individual, family)

    # Call validation functions
    validate_dates(individual, family)

if __name__ == '__main__':
    main()
