from helpers import calculate_years, get_name_id, date_compare, get_death
from helpers import get_birth, get_name_id_list, get_last_name, get_age
from helpers import find_duplicates, valid_divorce, siblings


def valid_tag(level, tag):
    """ Defines a dict of valid tags at each level,
        checks for a valid combination, and returns "Y" or "N"
    """
    valid_tags = {"0": ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
                  "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS",
                        "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
                  "2": ["DATE"]}

    return "Y" if level in valid_tags and tag in valid_tags[level] else "N"


def validate_genders(families, individuals):
    """ Identify families where traditional spouses don't exist. """
    husband_id = None
    wife_id = None
    all_good = True
    for spouse in families:
        husband_id = spouse['HUSB']
        wife_id = spouse['WIFE']

        for individual in individuals:
            if individual['ID'] == wife_id:
                if individual['SEX'] != 'F':
                    print("Anomaly US21: " +
                          "Wife %s in family (%s) is not female." %
                          (get_name_id(individual),
                           spouse['ID']))
                    all_good = False
            elif individual['ID'] == husband_id:
                if individual['SEX'] != 'M':
                    print("Anomaly US21: " +
                          "Husband %s in family (%s) is not male." %
                          (get_name_id(individual),
                           spouse['ID']))
                    all_good = False
    return all_good


def validate_males(families, individuals):
    """ Identify males in a given family with the same last name """
    valid = True
    for family in families:
        possible_males = []
        possible_males.append(family['HUSB'])
        for child in family['CHIL']:
            possible_males.append(child)

        last_name = ""
        for person in possible_males:
            for individual in individuals:
                if individual['ID'] == person:
                    if individual['SEX'] == 'M':
                        if last_name != "":
                            if (last_name != get_last_name(individuals,
                                                           individual['ID'])):
                                print("Anomaly US16: " +
                                      "Male %s has differing last name." %
                                      (get_name_id(individual)))
                                valid = False
                        else:
                            last_name = get_last_name(individuals,
                                                      individual['ID'])
    return valid


def validate_marriages(families, individuals):
    """ Verify all marriages are unique"""
    spouse_list = []
    duplicates = False

    for family in families:
        if family['DIV'] == '':
            spouse_list.append(family['WIFE'])
            spouse_list.append(family['HUSB'])

    spouse_duplicates = find_duplicates(spouse_list)

    for spouse in spouse_duplicates:
        duplicates = True
        for individual in individuals:
            if individual['ID'] == spouse:
                print("Anomaly US11: " +
                      "Spouse %s is a spouse in multiple families." %
                      (get_name_id(individual)))

    return duplicates


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


def valid_lifetime(birth, death):
    """ This routine validates the duration of life """
    if birth != '' and death != '':
        life_years = calculate_years(birth, death)
        if life_years < 150:
            return True
        else:
            return False


def validate_marriage_dates(family, indi_list):
    """ Verify marriage occurs before death of either spouse """
    wife_death = get_death(indi_list, family['WIFE'])
    husb_death = get_death(indi_list, family['HUSB'])
    marriage_date = family['MARR']

    if marriage_date == '':
        print("Error US05: Family %s has no marriage date." %
              (family['ID']))
        return 'no marriage'
    else:
        if wife_death != '' and date_compare(wife_death, marriage_date):
            print("Error US05: " +
                  "Marriage in family %s occurred after wife's death." %
                  (family['ID']))
            return 'after wife'
        if husb_death != '' and date_compare(husb_death, marriage_date):
            print("Error US05: " +
                  "Marriage in family %s occurred after husband's death." %
                  (family['ID']))
            return 'after husband'

    return 'no error'


def validate_marriage_divorce(family):
    """ Verify marriage and divorce occur in proper sequence """
    marriage_date = family['MARR']
    divorce_date = family['DIV']

    if marriage_date == '':
        print("Error US04: Family %s has no marriage date." %
              (family['ID']))
        return 'no marriage'
    elif divorce_date != '' and date_compare(divorce_date, marriage_date):
        print("Error US04: Marriage in family %s occurred after the divorce." %
              (family['ID']))
        return 'after divorce'

    return 'no error'


def validate_dates(fam_list, indi_list):
    for row in indi_list:
        birth_date = row["BIRT"]
        death_date = row["DEAT"]

        if not valid_month(birth_date):
            print("Error US42: Invalid birth month for %s" %
                  (get_name_id(row)))
        else:
            if not date_compare(birth_date, ''):
                print("Error US01: Birth date of" +
                      " %s occurs after the current date." %
                      (get_name_id(row)))
            if not date_compare(birth_date, death_date):
                print("Error US03: Birth date of" +
                      " %s occurs after the death date" %
                      (get_name_id(row)))
        # if death date was defined
        if not valid_month(death_date):
            print("Error US42: Invalid death month for %s" %
                  (get_name_id(row)))
        elif death_date != '':
            if not date_compare(row["DEAT"], ''):
                print("Error US01: Death date of" +
                      " %s occurs after the current date." %
                      (get_name_id(row)))
            if not valid_lifetime(birth_date, death_date):
                print("Error US07: Life duration of" +
                      " %s is greater than 150 years." %
                      (get_name_id(row)))

    for row in fam_list:
        marriage_date = row["MARR"]
        divorce_date = row["DIV"]

        # if marriage date was not defined - anomaly
        if marriage_date == '':
            print("Anomaly: No marriage date exists for family (%s)" %
                  (row['ID']))
        elif not valid_month(marriage_date):
            print("Error US42: Invalid marriage month for %s and %s" %
                  (get_name_id_list(indi_list, row["HUSB"]),
                   get_name_id_list(indi_list, row["WIFE"])))
        else:
            if not date_compare(marriage_date, ''):
                print("Error US01: Marriage date of %s and %s" %
                      (get_name_id_list(indi_list, row["HUSB"]),
                       get_name_id_list(indi_list, row["WIFE"])) +
                      " occurs after the current date.")
            # get birth date of the spouses
            wife_birth = get_birth(indi_list, row["WIFE"])
            husband_birth = get_birth(indi_list, row["HUSB"])
            if not date_compare(wife_birth, marriage_date):
                print("Error US02: Birth date of %s" %
                      (get_name_id_list(indi_list, row["WIFE"])) +
                      " occurs after the marriage date for family (%s)." %
                      row["ID"])
            if not date_compare(husband_birth, marriage_date):
                print("Error US02: Birth date of %s" %
                      (get_name_id_list(indi_list, row["HUSB"])) +
                      " occurs after the marriage date for family (%s)." %
                      row["ID"])

        # if divorce date was defined
        if not valid_month(divorce_date):
            print("Error US42: Invalid divorce month for %s and %s" %
                  (get_name_id_list(indi_list, row["HUSB"]),
                   get_name_id_list(indi_list, row["WIFE"])))
        else:
            if divorce_date != '' and not date_compare(divorce_date, ''):
                print("Error US01: Divorce date of %s and %s" %
                      (get_name_id_list(indi_list, row["HUSB"]),
                       get_name_id_list(indi_list, row["WIFE"])) +
                      " occurs after the current date.")

        # if children exist, check ages of parents at birth
        if row["CHIL"] != '':
            # get current age of parents
            dad_age = get_age(indi_list, row["HUSB"])
            mom_age = get_age(indi_list, row["WIFE"])
            for child in row["CHIL"]:
                child_age = get_age(indi_list, child)
                if (dad_age - child_age) >= 80:
                    print("Anomaly US12: Father %s" %
                          (get_name_id_list(indi_list, row["HUSB"])) +
                          " was older than 80 when %s was born." %
                          (get_name_id_list(indi_list, child)))
                elif (mom_age - child_age) >= 60:
                    print("Anomaly US12: Mother %s" %
                          (get_name_id_list(indi_list, row["WIFE"])) +
                          " was older than 60 when %s was born." %
                          (get_name_id_list(indi_list, child)))

        # validate marriage dates
        validate_marriage_divorce(row)
        validate_marriage_dates(row, indi_list)


def validate_ids(family, individual):
    """ Valid ID uniquness"""
    ids = []
    valid = True

    for row in individual:
        ids.append(row['ID'])

    for row in family:
        ids.append(row['ID'])

    duplicates = find_duplicates(ids)

    for entry in duplicates:
        valid = False
        print("Anomaly US22: ID %s is duplicated." % entry)

    return valid


def validate_name_birth(individual):
    """ Combinations of name and birth should be unique """
    name_birth_pairs = []
    valid = True

    for row in individual:
        name_birth = (row['NAME'], row['BIRT'])
        if name_birth not in name_birth_pairs:
            name_birth_pairs.append(name_birth)
        else:
            print("Anomaly US23: Name %s and Birth %s is duplicated" %
                  name_birth)
            valid = False

    return valid


def validate_divorces(families, individuals):
    """ Identify families where divorce occurred after one spouse died. """
    for spouse in families:
        if not valid_divorce(spouse, individuals):
            print("Error US06: Divorce in " +
                  "family %s occurred after death of one spouse." %
                  spouse['ID'])
    return True


def validate_siblings(families):
    """ Identify families where siblings married. """
    for spouse in families:
        if siblings(spouse['WIFE'], spouse['HUSB'], families):
            print("Anomaly US18: " +
                  "Spouses in family %s share at least one parent." %
                  spouse['ID'])
    return True
