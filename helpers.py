from collections import Counter
from datetime import date, datetime, timedelta
from math import floor


def is_deceased(row_death):
    """ Check if an individual is dead and return a Boolean value. """
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
        names of deceased people. """
    for row in indi_list:
        if is_deceased(row["DEAT"]):
            print('US29: Deceased: {0}, {1}'.format(row["NAME"], row['DEAT']))


def find_living_people_ids(individuals):
    """ Find all living people, then return a list of their ID and Name. """
    living_people_ids = []
    for person in individuals:
        if is_deceased(person["DEAT"]):
            continue
        else:
            living_people_ids.append([person["ID"], person["NAME"]])

    return living_people_ids


def get_currently_married(families):
    """ Takes a list of families as a parameter and checks if they are
        currently married by looking for an empty MARR, DIV row. Returns
        a list of couple IDs. """
    couple_ids = []
    for family in families:
        if family["MARR"] != '' and family["DIV"] == '':
            couple_ids.extend([family["HUSB"], family["WIFE"]])

    return couple_ids


def get_living_married(families, individuals):
    """ Return a list of living married people. """
    couple_ids = get_currently_married(families)
    living_people_ids = find_living_people_ids(individuals)
    living_married_people = []

    for living_person in living_people_ids:
        if living_person[0] in couple_ids:
            print("US30: Living married person: {}".format(living_person[1]))
            living_married_people.append([living_person[0], living_person[1]])

    return living_married_people


def list_living_single(individuals, families):
    """ List people over 30 years old who have never been married.
        Compare the ID of married people to living people over 30.
        If the person's ID is NOT IN the married people list,
        return the ID. """
    wife = None
    husb = None
    living_people_ids = []  # all living people
    family_ids = []  # all married or formerly married people
    living_single_people_over_30 = []

    for person in find_living_people_ids(individuals):
        living_people_ids.append(person[0])

    for family in families:
        wife = family["WIFE"]
        husb = family["HUSB"]
        family_ids.extend([wife, husb])

    for ID in living_people_ids:
        age = int(get_age(individuals, ID))
        if age > 30 and ID not in family_ids:
            living_single_people_over_30.append(ID)

    for person in find_living_people_ids(individuals):
        if person[0] in living_single_people_over_30:
            print("US31: Living single person over 30: {}, {}"
                  .format(person[0], person[1]))


def date_compare(date1, date2):
    """ This routine compares 2 dates in the Exact format
        and returns true if date1 is before date2; otherwise, returns false
        by default, the later date is set to today.
    """
    early_date = datetime.strptime(date1, '%d %b %Y').date()
    if date2 == '':
        late_date = datetime.now().date()
    else:
        late_date = datetime.strptime(date2, '%d %b %Y').date()

    if early_date < late_date:
        return True
    else:
        return False


def get_recent_deaths(individuals):
    """ Return a list of individuals who've died within the last 30 days.
        Return -1 if individuals have not died within the last 30 days. """
    today = datetime.now()
    DD = timedelta(days=30)
    names = []
    for individual in individuals:
        if individual["DEAT"]:
            dday = datetime.strptime(individual["DEAT"], '%d %b %Y')
            days = today - dday
            if days <= DD and dday < today:
                print('US36: Recent Death: {} | {}'.format(individual['NAME'],
                      dday.strftime('%d %b %Y')))
                names.append(individual["NAME"])
    return names


def get_recent_births(individuals):
    """ Return a list of individuals who've been born within the last 30 days.
        Return -1 if individuals were not born within the last 30 days. """
    today = datetime.now()
    DD = timedelta(days=30)
    names = []
    for individual in individuals:
        try:
            bday = datetime.strptime(individual["BIRT"], '%d %b %Y')
            days = today - bday
            if days < DD and bday < today:
                print('US35: Recent Birth: {} | {}'.format(individual['NAME'],
                       bday.strftime('%d %b %Y')))
                names.append(individual["NAME"])
        except ValueError:
            # Invalid date, carry on
            pass
    return names


def get_name(list, id):
    """ Get the name for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"


def get_last_name(list, id):
    name = get_name(list, id)
    names = name.split('/')

    if len(names) > 1:
        return names[-2]
    else:
        return "Unknown"


def get_age(list, id):
    """ This returns the the age of a given individual """
    for row in list:
        if row["ID"] == id:
            birth_date = row["BIRT"]
            today = datetime.now().date().strftime('%d %b %Y')
            return calculate_years(birth_date, today)
    return -1


def get_birth(list, id):
    """ Get the birth date for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["BIRT"]
    return "Unknown"


def get_death(list, id):
    """ Get the death date for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["DEAT"]
    return "Unknown"


def calculate_years(date1, date2):
    """ this returns the number of years between 2 exact format dates """
    try:
        first_date = datetime.strptime(date1, '%d %b %Y').date()
        second_date = datetime.strptime(date2, '%d %b %Y').date()

        years = (first_date - second_date).days / 365
        return floor(abs(years))
    except ValueError:
        return 0


def get_name_id(indi):
    """ return name and ID for printing """
    out_string = indi["NAME"] + ' (' + indi["ID"] + ')'
    return out_string


def get_name_id_list(list, id):
    """ return name and ID for printing """
    for row in list:
        if row["ID"] == id:
            out_string = row["NAME"] + ' (' + row["ID"] + ')'
            return out_string
    return "Unknown"


def find_duplicates(list):
    """ Find duplicates in list, return list with duplicate values"""
    return [item for item, count in Counter(list).items() if count > 1]


def valid_divorce(family, indi_list):
    """ returns false if one spouse died before the divorce. """
    divorce_date = family['DIV']
    if divorce_date == '':
        return True
    else:
        husband_death = get_death(indi_list, family['HUSB'])
        wife_death = get_death(indi_list, family['WIFE'])
        if ((husband_death != '' and
             date_compare(husband_death, divorce_date)) or
            (wife_death != '' and
             date_compare(wife_death, divorce_date))):
            return False
        else:
            return True


def get_mom(indi, fam_list):
    """ returns ID of the individual's mother """
    for family in fam_list:
        for child in family['CHIL']:
            if indi == child:
                return family['WIFE']
    return 'unknown'


def get_dad(indi, fam_list):
    """ returns ID of the individual's father """
    for family in fam_list:
        for child in family['CHIL']:
            if indi == child:
                return family['HUSB']
    return 'unknown'


def siblings(indi1, indi2, fam_list):
    """ returns true if the input individuals share a parent,
    returns false otherwise (even if undetermined) """
    mom1 = get_mom(indi1, fam_list)
    mom2 = get_mom(indi2, fam_list)
    dad1 = get_dad(indi1, fam_list)
    dad2 = get_dad(indi2, fam_list)

    if (mom1 == mom2 and mom1 != 'unknown'):
        return True
    elif (dad1 == dad2 and dad1 != 'unknown'):
        return True
    else:
        return False


def sort_siblings(children, individuals):
    """ Sorts the given list by decreasing age """
    children.sort(key=lambda x: get_age(individuals, x), reverse=True)
