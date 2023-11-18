import datetime
import logging
import pandas as pd

"""Hi, This is a function set that verify all the inputs.
You can simply use them to replace the input() functions."""

# Creating list of valid cities in the world.
# The csv file comes from the World Cities Database by SimpleMaps.com, last updated: March 31, 2023.
# The file contains data for about 43 thousand cities.
valid_cities_csv = pd.read_csv('worldcities.csv')
valid_cities = valid_cities_csv['City'].list()


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
    while True:
        # first checks that location is a string
        _location = string(line)
        if _location in valid_cities:
            return _location
        else:
            logging.error(f'Location {_location} input by user is not a valid city in the database.')
            print("Location needs to be a valid city. Please try again.")


def name(line):
    while True:
        # first checks that name is a string
        _name = string(line)
        if all(character.isalpha() or character == '-' for character in _name):
            return _name
        else:
            logging.error(f'Name {_name} input by user is not in the correct format.')
            print("Please make sure you only input letters.")


def email(line):
    while True:
        # first checks that email is a string
        _email = string(line)
        if '@' in _email and all(email.split('@')):
            return _email
        else:
            logging.error(f'Email {_email} input by user is not in the correct format.')
            print("Please make sure email is in this format: example@email.com.")


def main():
    ...


if __name__ == "__main__":
    main()
