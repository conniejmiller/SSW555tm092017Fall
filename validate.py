from datetime import datetime
from helpers import *


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
                    print('Anomaly US21: Wife ' +
                          individual['NAME'] + ' (' + individual['ID'] + ') ' +
                          'in family ' + spouse['ID'] + 'is not female.')
                    all_good = False
            elif individual['ID'] == husband_id:
                if individual['SEX'] != 'M':
                    print('Anomaly US21: Husband ' +
                          individual['NAME'] + ' (' + individual['ID'] + ') ' +
                          'in family ' + spouse['ID'] + 'is not male.')
                    all_good = False
    return all_good


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
        death_date = datetime.strptime(death, '%d %b %Y').date()
        birth_date = datetime.strptime(birth, '%d %b %Y').date()

        life_years = (death_date - birth_date).days / 365
        if life_years < 150:
            return True
        else:
            return False


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
                  get_name(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  get_name(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ')')
        elif not date_compare(row["MARR"]):
            print('Error US01: Marriage date of ' +
                  get_name(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  get_name(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ') occurs after the current date.')

        # if divorce date was defined
        if not valid_month(row["DIV"]):
            print('Error US42: Invalid divorce month for ' +
                  get_name(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  get_name(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
                  ')')
        elif row["DIV"] != '' and not date_compare(row["DIV"]):
            print('Error US01: Divorce date of ' +
                  get_name(indi_list, row["HUSB"]) + ' (' + row["HUSB"] +
                  ') and ' +
                  get_name(indi_list, row["WIFE"]) + ' (' + row["WIFE"] +
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
                          get_name(indi_list, row["HUSB"]) +
                          ' (' + row["HUSB"] +
                          ') was older than 80 when ' +
                          get_name(indi_list, child) + ' (' + child +
                          ') was born.')
                elif (mom_age - child_age) >= 60:
                    print('Anomaly US12: Mother ' +
                          get_name(indi_list, row["WIFE"]) +
                          ' (' + row["WIFE"] +
                          ') was older than 60 when ' +
                          get_name(indi_list, child) + ' (' + child +
                          ') was born.')
