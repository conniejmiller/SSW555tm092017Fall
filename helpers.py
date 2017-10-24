from math import floor
from datetime import datetime, timedelta


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
            print('US29: Deceased: {0}, {1}'.format(row["NAME"], row['DEAT']))


def date_compare(date1, date2):
    """ This routine compares 2 dates in the Exact format 
        and returns true if the early date is before thelater date
        otherwise, returns false
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
    past_30_days = datetime.now().date() + timedelta(days=-30)
    for individual in individuals:
        if is_deceased(individual["DEAT"]):
            dt = datetime.strptime(individual["DEAT"], '%d %b %Y').date()
            if dt >= past_30_days and dt <= datetime.now().date():
                print('US36: LIST RECENT DEATHS: {} | {}'.format(individual["NAME"],dt))
                return 'US36: LIST RECENT DEATHS: {} | {}'.format(individual["NAME"],dt)
        return -1


def get_recent_births(individuals):
    """ Return a list of individuals who've been born within the last 30 days. 
        Return -1 if individuals were not born within the last 30 days. """ 
    past_30_days = datetime.now().date() + timedelta(days=-30)
    for individual in individuals:
        if individual["BIRT"]:
            dt = datetime.strptime(individual["BIRT"], '%d %b %Y').date()
            if dt >= past_30_days and dt <= datetime.now().date():
                print('US35: LIST RECENT BIRTHS: {} | {}'.format(individual["NAME"],dt))
                return 'US35: LIST RECENT BIRTHS: {} | {}'.format(individual["NAME"],dt)
        return -1


def get_name(list, id):
    """ Get the name for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"


def get_birth(list, id):
    """ Get the birth date for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["BIRT"]
    return "Unknown"


def calculate_years(date1, date2):
    # this returns the number of years between 2 exact format dates
    first_date = datetime.strptime(date1, '%d %b %Y').date()
    second_date = datetime.strptime(date2, '%d %b %Y').date()

    years = (first_date - second_date).days / 365
    return floor(abs(years))


