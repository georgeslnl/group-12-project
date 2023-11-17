import datetime
import logging

"""Hi, This is a function set that verify all the inputs.
You can simply use them to replace the input() functions."""


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


def main():
    ...


if __name__ == "__main__":
    main()
