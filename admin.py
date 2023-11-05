import pandas as pd
from datetime import datetime
from humanitarianplan import HumanitarianPlan


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
           The admin needs to input a description, the location affected, the start date of the event, and the number
           of camps.
           The method then creates a new HumanitarianPlan object and returns it.
           It also adds the Humanitarian Plan to the csv file 'humanitarian_plan.csv'
           """

        # Asking for user input, using while loops and exception handling to ensure correct format.
        # (ensures input is not empty and is of the correct data type)
        # future aim: code to avoid duplicate plans (if description, location and date are all the same then a new plan
        # should not be created).
        while True:
            try:
                desc = input("Please enter a description of the event: ").strip()
                # strip() in case the input is a space to trick the system as a useful string.
                if not desc:  # if desc is empty
                    raise ValueError('No data was entered.')  # raise an error is more direct in this case
                if float(desc):  # if desc is a number
                    raise ValueError('Please make sure description is of correct data type.')
            except ValueError as e:
                print(e)
                continue
            break

        while True:
            try:
                loc = input("Please enter the geographical location affected: ").strip()
                if not loc:  # if desc is empty
                    raise ValueError('No data was entered.')
                if float(loc):  # if loc is a number
                    raise ValueError('Please make sure description is of correct data type.')
            except ValueError as e:
                print(e)
                continue
            break

        while True:
            try:
                start_date = input("Please enter the start date of the event (DD-MM-YYYY): ").strip()
                # remind of the format DD-MM-YYYY
                if not start_date:
                    raise ValueError("No data was entered.")
                try:
                    datetime.strptime(start_date, "%d-%m-%Y")  # no need for check variable
                    break
                except ValueError:
                    print("Date must be in (DD-MM-YYYY) format. Please try again.")
                    continue  # added continue because print doesn't continue the loop
            except Exception as e:
                print(e)
                continue
            break

        while True:
            try:
                nb_of_camps = input("Please enter the number of camps to set up: ").strip()
                if not nb_of_camps:
                    raise ValueError("Please enter a data.")
                if not nb_of_camps.isdigit():  # check if it is an integer
                    raise ValueError('Please enter an integer.')
            except Exception as e:
                print(e)
                continue
            break

        # Creating humanitarian plan object
        hu_pl = HumanitarianPlan(desc, loc, start_date, nb_of_camps)

        # Opens the csv file and adds the data for this humanitarian plan
        h = open("humanitarian_plan.csv", "a")
        h.write(f'\n"{desc}",{loc},{start_date},{nb_of_camps}')
        # desc is wrapped in "" because we don't want to csv file to see a "," in the description as a delimitter
        h.close()

        # Prints out the information about the Humanitarian Plan created
        print(f'A new humanitarian plan has been created with the following information:'
              f'\n\t Description: {desc}'
              f'\n\t Location affected: {loc}'
              f'\n\t Start of the event: {start_date}'
              f'\n\t Number of camps: {nb_of_camps}')

        return hu_pl

    def display_hum_plan(self, hum_plan):
        """
        This method displays summary information about the humanitarian plan.
        Information to display:
            - Number of refugees
            - Their camp identification
            - Number of volunteers working at each camp
        """
        # what is the hum_plan input?
        # humanitarian_plan = pd.read_csv('humanitarian_plan.csv')
        camps = pd.read_csv('camps.csv')
        print('Total number of refugees: ', sum(camps['refugees']))
        print('Camp ID of camps involved: \n', camps['camp_name'])
        print('Number of volunteers working at each camp: \n', camps[['camp_name', 'volunteers']])

    def creat_volunteer(self):  # TODO exception handling
        new = open("users.csv", "a")

        username = input("Please enter an user name: ").strip()
        pw = input("Please enter the password: ").strip()
        first_name = input("Please enter the first name: ").strip()
        last_name = input("Please enter the last name: ").strip()
        phone = input("Please enter the phone number: ").strip()
        address = input("Please enter the address: ").split(",").strip()
        # TODO: sort out how the coma in address will work in the csv file
        DOB = input("Please enter the date of birth (DD-MM-YYYY): ").strip()
        camp_name = input("Please enter an user name: ").strip()
        status = "A"  # status is active by default

        new.write(f'\n"{username}",{pw},{first_name},{last_name},{phone},{address},{DOB},{camp_name},{status}')
        new.close()

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
                print("Date must be in DD-MM-YYYY format. Please try again.")

        hum_plan.end_date = end
        return hum_plan


# admin username and password have been hardcoded here
# login process
admin_authorised = False
while admin_authorised == False:
    username_attempt = input("Enter username.")
    password_attempt = input("Enter password.")
    if username_attempt == 'admin' and password_attempt == '111':
        admin_authorised = True
        try:
            admin = Admin('admin', '111')
        except ValueError as e:
            print(e)  # If login details are incorrect, admin user will not be created
        else:
            print(admin)
            # list of functions for admin to choose what to do, exception handling to ensure correct format
            choice_format = False
            while choice_format == False:
                action = input('Enter what you would like to do.'
                               '\n 1 for creating a humanitarian plan'
                               '\n 2 for ending a humanitarian plan'
                               '\n 3 for displaying the humanitarian plan'
                               '\n 4 for editing a volunteer account'
                               '\n 5 for creating a volunteer account'
                               '\n 6 for deleting a volunteer account'  # adding a deleting feature
                               '\n 7 for deactivating and reactivating a volunteer account'
                               # just trying to list all branches here to avoid creating too many branches in 
                               # option 4, what do you think?
                               '\n 8 for allocating resources')
                try:
                    action = int(action)
                    if action in range(1, 8):
                        choice_format = True
                except ValueError:
                    print('Please enter an integer from 1-6.')
            if action == 1:
                humanitarian_plan = admin.create_hum_plan()
            if action == 3:
                admin.display_hum_plan('hum_plan')
    else:
        print("Wrong username or password entered.")
