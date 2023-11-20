import re, logging, datetime
import verify as v

def add_description():
    while True:
        print("\nEnter [0] to return to the previous menu.")
        try:
            desc = input("Please enter a description of the event: ").strip()
            if desc == "0":
                return desc
            s = re.search("[a-zA-Z]", desc)
            if not s:
                raise ValueError
        except ValueError:
            print("Please ensure description contains text.")
            continue
        if len(desc) > 200:
            print("Description cannot exceed 200 characters.")
            continue
        return desc

def add_location():
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        try:
            loc = input("Please enter the location (city) of the event: ").strip()
            if loc in ("0", "9"):
                return loc
            s = re.search("[a-zA-Z]", loc)
            if not s:
                raise ValueError
        except ValueError:
            print("Please ensure location contains text.")
            continue
        if loc.lower() not in v.valid_cities:
            print("The city you have entered does not exist. Please try again.")
            continue
        return loc

def add_start_date():
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        start_date = input("Please enter the start date of the event (DD-MM-YYYY): ").strip()
        if start_date in ("0", "9"):
            return start_date
        try:
            start = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
        except ValueError:
            print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
            continue
        t = datetime.date.today()
        if start > t:
            print("Start date cannot be in the future. Please try again.")
            continue
        if start < t - datetime.timedelta(days=30):
            while True:
                print("\nWarning: More than 30 days have elapsed since the start date.")
                print("Do you wish to proceed?")
                print("Enter [1] to proceed")
                print("Enter [9] to re-enter start date")
                try:
                    option = int(input("Select an option: "))
                    if option not in (1, 9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break
            if option == 9:
                continue
        return start_date

def add_num_camps():
    while True:
        print("\nEnter [X] to return to the previous menu or B] to go back to the previous step.")
        nb_of_camps = input("Please enter the number of camps to set up: ").strip()
        if nb_of_camps in ("X", "B"):
            return nb_of_camps
        try:
            nb_of_camps = int(nb_of_camps)
            if nb_of_camps <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a positive integer.")
            continue
        return nb_of_camps