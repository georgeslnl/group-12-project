import pandas as pd
from datetime import datetime


class Admin:
    """Class for the Admin user. Since there can only be 1 admin, this class can only be initialised once"""

    def __init__(self, username, password):
        if username != 'admin' or password != '111':  # Checks if password and username are correct
            raise ValueError('Login failed')
        else:
            self.username = username  # if login credentials are correct, admin object is initialised
            self.password = password

    def create_hum_plan(self):
        """This method lets the admin create a new humanitarian plan.
           The admin needs to input a description, the location affected, and the start date of the event.
           The method then creates a new HumanitarianPlan object and returns it.
           It also adds the Humanitarian Plan to the csv file 'humanitarian_plan.csv'
           """

        # Asking for user input, using while loops and exception handling to ensure correct format.
        while True:
            try:
                desc = input("Please enter a description: ")
                break
            except ValueError:
                print('Please make sure description is of correct type.')
            except Exception as e:
                print(e)
        while True:
            try:
                loc = input("Please enter the geographical location affected: ")
                break
            except ValueError:
                print('Please make sure description is of correct type.')
            except Exception as e:
                print(e)
        while True:
            try:
                start_date = input("Please enter the start date of the event: ")
                check = datetime.strptime(start_date, "%d-%m-%Y")
                break
            except ValueError:
                print("Date must be in (DD-MM-YYYY) format. Please try again.")

        # Creating humanitarian plan object
        hu_pl = HumanitarianPlan(desc, loc, start_date)

        # Opens the csv file and adds the data for this humanitarian plan
        h = open("humanitarian_plan.csv", "a")
        h.write(f'\n"{desc}",{loc},{start_date}')
        # desc is wrapped in "" because we don't want to csv file to see a "," in the description as a delimitter
        h.close()

        # Prints out the information about the Humanitarian Plan created
        print(f'A new humanitarian plan has been created with the following information:'
              f'\n\t Description: {desc}'
              f'\n\t Location affected: {loc}'
              f'\n\t Start of the event: {start_date}')

        return hu_pl

    def display_hum_plan(self, hum_plan):
        """
        This method displays summary information about the humanitarian plan.
        Information to display:
            - Number of refugees
            - Their camp identification
            - Number of volunteers working at each camp
        """
        pass

    def end_event(self, hum_plan):
        """
        This method requires a HumanitarianPlan object as argument.
        The method then updates the end_date attribute to the input date from the admin.

        The while loop is used to ensure the user inputs a date in the correct format
        """

        while True:
            end = input('Please input the end date of the event: (DD-MM-YYYY) ')
            try:
                check = datetime.strptime(end, "%d-%m-%Y")
                break
            except ValueError:
                print("Date must be in (DD-MM-YYYY) format. Please try again.")

        hum_plan.end_date = end
        return hum_plan


class HumanitarianPlan:
    """
    Class for the Humanitarian Plan. It requires a description, location, and start_date, which are passed as arguments
    from create_hum_plan method of Admin class.

    When initialised, end_date is set to 'None' and can later be edited with edit_end_date method of Admin class
    """
    def __init__(self, description, location, start_date):
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = None


# username and password have been hardcoded here, but in the main file the user will have to input the values
# which will then be passed as arguments in the object creation
try:
    admin = Admin('admin', '111')
except ValueError as e:
    print(e)  # If login details are incorrect, admin user will not be created
else:
    print(admin)
    humanitarian_plan = admin.create_hum_plan()