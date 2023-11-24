import datetime
import logging
import pandas as pd, numpy as np, re, datetime


"""This is a function set that verify all the inputs to include all exception handling.
You can simply use them to replace the input() functions.
"""

# Creating list of valid cities in the world.
# The csv file comes from the World Cities Database by SimpleMaps.com, last updated: March 31, 2023.
# The file contains data for about 43 thousand cities.
valid_cities_csv = pd.read_csv('worldcities.csv')
valid_cities = valid_cities_csv['city'].tolist()
valid_cities = [city.lower() for city in valid_cities]

def integer(line):
    while True:
        try:
            _int = input(line).strip()
            if not _int:  # if int is empty
                raise ValueError('No data was entered.')
            if not _int.isdigit():  # if int is not a number
                raise ValueError('Please enter an integer.')
            return int(_int)
        except ValueError as e:
            logging.error('ValueError raised from user input')
            print(e)


def string(line):
    while True:
        try:
            _str = input(line)
            if _str == "0":
                return _str
            _str[0]
            try:
                float(_str)
                print('Please make sure data entered is of correct data type.')
            except ValueError:
                logging.error('ValueError raised from user input')
                break
        except IndexError:
            logging.error('IndexError raised from user input')
            print('No data was entered.')
        except Exception as e:
            logging.error(f'Error raised from user input: {e}')
            print(e)
    return _str


def date(line):
    while True:
        _date = input(line).strip()
        if _date == "0":
            return _date
        if not _date:
            print("No data was entered. Please enter a date.")
            continue
        try:
            _date = datetime.datetime.strptime(_date, "%d-%m-%Y")
            return _date.date()
        except ValueError:
            logging.error('ValueError raised from user input')
            print("Date must be in (DD-MM-YYYY) format. Please try again.")


def location(line):
    if line == 0:
        return line
    else:
        while True:
            # first checks that location is a string
            _location = string(line)
            if _location.lower() in valid_cities:
                return _location
            else:
                logging.error(f'Location {_location} input by user is not a valid city in the database.')
                print("Location needs to be a valid city. Please try again.")


def name(line):
    while True:
        # first checks that name is a string
        _name = string(line).strip()
        s = re.search("^[a-zA-Z-' ]+$", _name)
        if _name == "0":
            return _name
        elif _name == "":
            logging.error('User did not enter a name.')
            print("Please enter a name.")
        if not s:
            logging.error(f'Name {_name} input by user is not in the correct format.')
            print("Name can only contain letters, hyphen (-) and apostrophe (').")
        else:
            return _name

def username(line):
    while True:
        _username = input(line).strip()
        s = re.search("^[a-zA-Z]+[a-zA-Z0-9_]*$", _username)
        users = pd.read_csv('users.csv', dtype={'password': str})
        select_username = users[users['username'] == _username]
        if _username == "0":
            return _username
        elif _username == "":
            logging.error("User did not enter a username.")
            print("Please enter a username.")
        elif not s:
            logging.error(f'Username {_username} input by user is not in the correct format.')
            print("Username can only contain letters, digits (0-9) and underscore (_), and must start with a letter. Please choose another username.")
        elif 0 < len(select_username.index):  # username already exists
            print("Username is taken. Please choose another username.")
            logging.error("User entered a username that already exists.")
        else:
            return _username

def email(line):
    while True:
        # first checks that email is a string
        _email = string(line)
        s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", _email)
        if _email == "0":
            return _email
        elif _email == "":
            logging.error("User did not enter an email address.")
            print("Please enter an email address.")
        elif not s:
            logging.error(f'Email {_email} input by user is not in the correct format.')
            print("Please make sure email is in this format: example@email.com.")
        else:
            return _email

def phone_number(line):
    while True:
        _number = input(line).strip()
        s = re.search("^\+?\d{1,3} \d{8,11}$", _number)  # allow starting + to be omitted
        if _number == "0":
            return _number
        elif _number == "":
            logging.error("User did not enter a phone number.")
            print("Please enter a phone number.")
        elif _number[0] != "+":
            _number = f"+{_number}"
            return _number
        elif not s:
            logging.error(f'Phone number {_number} input by user is not in the correct format.')
            print("Incorrect phone number format. Please try again.")
        else:
            return _number



def main():
    ...


if __name__ == "__main__":
    main()
