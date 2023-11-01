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
                desc = input("Please enter a description of the event: ")
                desc[0]
                try:
                    float(desc)
                    print('Please make sure description is of correct data type.')
                except ValueError:
                    break
            except IndexError:
                print('No data was entered.')
            except Exception as e:
                print(e)
        while True:
            try:
                loc = input("Please enter the geographical location affected: ")
                loc[0]
                try:
                    float(loc)
                    print('Please make sure location entered is of correct data type.')
                except ValueError:
                    break
            except IndexError:
                print('No data was entered.')
            except Exception as e:
                print(e)
        while True:
            try:
                start_date = input("Please enter the start date of the event: ")
                start_date[0]
                try:
                    check = datetime.strptime(start_date, "%d-%m-%Y")
                    break
                except ValueError:
                    print("Date must be in (DD-MM-YYYY) format. Please try again.")
            except IndexError:
                print('No data was entered.')
            except Exception as e:
                print(e)
        while True:
            try:
                nb_of_camps = input("Please enter the number of camps to set up: ")
                nb_of_camps[0]
                try:
                    int(nb_of_camps)
                    break
                except ValueError:
                    print('Please make sure you have entered a number.')
            except IndexError:
                print('No data was entered.')
            except Exception as e:
                print(e)

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
    Class for the Humanitarian Plan. It requires a description, location, start_date and nb_of_camps which are passed
    as arguments from create_hum_plan method of Admin class.

    nb_of_camps is the number of camps created when the Humanitarian Plan is created. The admin should specify how
    many camps should be set up.

    When initialised, end_date is set to 'None' and can later be edited with edit_end_date method of Admin class.

    When initialised, a resources csv file is created with a row for the number of camps specified
    """

    def __init__(self, description, location, start_date, nb_of_camps):
        self.description = description
        self.location = location
        self.start_date = start_date
        self.name = location + start_date[6:]  # name would be location + year e.g. United Kingdom 2023
        self.nb_of_camps = int(nb_of_camps)
        self.end_date = None

        # When a Humanitarian Plan object is created, it also creates a resources csv for that HP
        create = open(f"{self.name}_resources.csv", "w")
        create.write("Camp ID,Food Packs,Water,First-Aid Kit"
                     "\nStorage,100,100,25")
        create.close()

        # Adds the rows for each camp into the resources.csv file, based on how many camps exist
        # e.g. if nb_of_camps is 3, there will be a row added to the csv for Camp 1, Camp 2, and Camp 3
        add_camps = open(f"{self.name}_resources.csv", "a")
        for i in range(1, self.nb_of_camps + 1):  # starts at 1 since default is 0 and doesn't make sense to have Camp 0
            add_camps.write(f"\nCamp {i},0,0,0")  # at the start, each camp has 0 of every resource type


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
            # Insert list of functions for admin to choose what to do
            humanitarian_plan = admin.create_hum_plan()
    else:
        print("Wrong username or password entered.")

