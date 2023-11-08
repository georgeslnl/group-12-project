import datetime

"""Hi, This is a function set that verify all the inputs
You can simply use the to replace the input() functions."""

def integer(line):
    while True:
        try:
            _int = input(line).strip()
            if not _int:  # if int is empty
                raise ValueError('No data was entered.')
            if not _int.isdigit():  # if int is not a number
                raise ValueError('Please enter an integer.')
            return _int
        except ValueError as e:
            print(e)

def string(line):
    while True:
        try:
            _str = input(line).strip()
            if not _str:  # if the input is empty
                raise ValueError('No data was entered.')
            if _str.isdigit():  # if input is a number
                raise ValueError('Please make sure description is of correct data type.')
            return _str
        except ValueError as e:
            print(e)

def date(line):
    while True:
        _date = input(line).strip()
        if not _date:
            print("No data was entered. Please enter a date.")
            continue
        try:
            _date = datetime.strptime(_date, "%d-%m-%Y")
            return _date
        except ValueError:
            print("Date must be in (DD-MM-YYYY) format. Please try again.")

def main():
    ...

if __name__ == "__main__":
    main()