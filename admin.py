import pandas as pd
from datetime import datetime
from humanitarianplan import HumanitarianPlan
import verify as v
import logging


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
                loc = input("Please enter the location of the event: ")
                loc[0]
                try:
                    float(loc)
                    print('Please make sure description is of correct data type.')
                except ValueError:
                    logging.error('ValueError raised from user input')
                    break
            except IndexError:
                logging.error('IndexError raised from user input')
                print('No data was entered.')
            except Exception as e:
                logging.error(f'Error raised from user input: {e}')
                print(e)

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
                    logging.error('ValueError raised from user input')
                    print("Date must be in (DD-MM-YYYY) format. Please try again.")
                    continue  # added continue because print doesn't continue the loop
            except Exception as e:
                logging.error(f'Error raised from user input: {e}')
                print(e)
                continue

        while True:
            try:
                nb_of_camps = input("Please enter the number of camps to set up: ").strip()
                if not nb_of_camps:
                    logging.error('ValueError raised from user input')
                    raise ValueError("Please enter a data.")
                if not nb_of_camps.isdigit():  # check if it is an integer
                    logging.error('ValueError raised from user input')
                    raise ValueError('Please enter an integer.')
            except Exception as e:
                logging.error(f'Error raised from user input: {e}')
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
        hu_pl = pd.read_csv('%s.csv' %(hum_plan))
        print('Total number of refugees: ', sum(hu_pl['refugees']))
        print('Camp ID of camps involved: \n', hu_pl['camp_name'])
        print('Number of volunteers working at each camp: \n', hu_pl[['camp_name', 'volunteers']])

    def edit_volunteer(self):
        df = pd.read_csv('users.csv')
        # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
        print(df.iloc[1:, 0])
        while True:
            user = v.string('Please enter the username of the volunteer whose account details you would like to modify.')
            if any(df['username'].str.contains(user)) == True: #testing if volunteer account already exists
                break
            else:
                print('Username entered does not match with any volunteer.')
                continue
        while True:
            # a list for admin to choose from, edited to work for the merged 'users' file
            print("Please choose one of the following details you would like to modify."
                  "\n 0 for username"
                  "\n 1 for password"
                  "\n 2 for active status"
                  "\n 3 for first name"
                  "\n 4 for last name"
                  "\n 5 for email address"
                  "\n 6 for phone number"
                  "\n 7 for gender"
                  "\n 8 for date of birth"
                  "\n 9 for plan ID"
                  "\n 10 for camp name")
            index = int(v.integer(""))
            if index not in range(0, 11):
                print('Please enter an integer from 0-10.')
                continue
            else:
                #This is code to fix the index problem due to using the new 'users' file
                if index==2:
                    index=3
                elif index==0 or index==1:
                    pass
                else:
                    index+=2
                break
        temp_list = ['username', 'password', 'account_type', 'active_status', 'deactivation_requested',
                     'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'plan_id', 'camp_name']
        new = input("Please enter a new value: ")  # will be used to input into csv as status
        # and then enter a new value
        # create a dataform without that specific row where username is...
        df.loc[df['username'] == user, temp_list[index]] = new  # modify the dataform
        df.to_csv('users.csv', index=False)  # write it into the .csv file
        updated = df['username'] == user
        print("The updated account details of " + user + "is:\n", df[updated])

    def create_volunteer(self):
        new = open("users.csv", "a")

        username = v.string("Please enter an user name: ")
        pw = input("Please enter the password: ") #password should be just '111'
        first_name = v.string("Please enter the first name: ")
        last_name = v.string("Please enter the last name: ")
        email = v.string("PLease enter the email address: ")
        phone = v.integer("Please enter the phone number: ")
        gender = v.integer("Please enter the gender: ")
        DOB = v.date("Please enter the date of birth (DD-MM-YYYY): ")
        plan_id = v.string("Please enter the plan ID: ")
        camp_name = v.string("Please enter the camp name: ")

        new.write(f'\n{username},{pw},volunteer,1,0,{first_name},{last_name},{email},{phone},{gender},{DOB},{plan_id},{camp_name}')
        new.close()
        print("New user added successfully.")

        users = pd.read_csv('users.csv')
        new_account = users['username'] == username
        print("The new account details of", username, "is:\n", users[new_account])

    def delete_volunteer(self):
        df = pd.read_csv('users.csv')
        # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
        print(df.iloc[1:, 0])
        while True:
            delete_user = v.string('Please enter the username you would like to delete. ')
            if any(df['username'].str.contains(delete_user)) == False:  # testing if volunteer account already exists
                print("Username not found. Please enter again.")
            else:
                break
        # create a dataform without that specific row where username is...
        df = df[df.username != delete_user]
        df.to_csv('users.csv', index=False)
        print(f"{delete_user} is now deleted.")
        logging.info(f'{delete_user} deleted by Admin')
        print(df)

    def active_volunteer(self):
        while True:
            status = v.string("Would you like to deactivate or reactivate an user? (D/R)"
                              "\n D for deactivate"
                              "\n R for reactivate")
            if status != "R" and status != "D":
                print("Please enter only D or R.")
            elif status == "R":
                status = "1"    #input this into the csv
                request = "0"
                _str = "reactivate"
                break
            elif status == "D":
                status = "0"
                _str = "deactivate"
                request = "0"
                break

        df = pd.read_csv('users.csv')
        # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
        print(df.iloc[1:, 0])
        while True:
            user = v.string(f'Please enter the username you would like to {_str}. ')
            if any(df['username'].str.contains(user)) == False:  # testing if volunteer account already exists
                print("Username not found. Please enter again.")
            else:
                break
        df.loc[df['username'] == user, 'status'] = status  # modify the dataform
        df.loc[df['username'] == user, 'active'] = request
        df.to_csv('users.csv', index=False)  # write it into the .csv file

        print(f'Complete. {user} is now modified.'
              "All status below:")
        print(df)
        logging.info({f'Admin has {_str}d {user}'})

    def check_deactivation_requests(self):
        """
        This method tells the Admin if volunteers have requested to deactivate their
        account, and informs the Admin of the steps to take.
        This is done by reading the users.csv file and calling the deactivate_account_request() method

        """
        users = pd.read_csv('users.csv', dtype={'password': str})
        nb_of_requests = len(users[users["deactivation_requested"] == 1])
        # prints if there are 0 requests to deactivate account
        if nb_of_requests == 0:
            print('No new deactivation requests.')
            return
        elif nb_of_requests == 1:
            print('You have received a deactivation request')
            # extracts the username of the user who requested deactivation
            user_deactivating = users.loc[users['deactivation_requested'] == 1, 'username'].item()
            # calls method to deactivate the account
            self.deactivate_account_request(df=users, user=user_deactivating)
            # saves changes to the users.csv file
            users.to_csv('users.csv', index=False)
            print('The deactivation request has been processed!')
        else:
            print(f'You have received {nb_of_requests} deactivation requests')
            # extracts the usernames of users that requested deactivation into a list
            users_deactivating = users.loc[users['deactivation_requested'] == 1, 'username'].tolist()
            # calls the deactivation method for each username in the list
            for username in users_deactivating:
                self.deactivate_account_request(df=users, user=username)
            # saves the changes to the list
            users.to_csv('users.csv', index=False)
            print('All deactivation requests have been processed!')

    def deactivate_account_request(self, df, user):
        """This method is called when an Admin wants to deactivate a volunteer's account following a request"""
        while True:
            print(f'User {user} has requested to deactivate their account.')
            print('Enter [1] to deactivate the account')
            print('Enter [2] to keep the account active')
            try:
                option = int(input("Select an option: "))
                if option not in (1, 2):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        # admin chose to deactivate account
        if option == 1:
            df.loc[df['username'] == user, ['deactivation_requested', 'active']] = 0
            print(f'You have deactivated {user}')
            logging.info(f'Admin has deactivated {user}')
        # admin chose to keep account active
        else:
            df.loc[df['username'] == user, 'deactivation_requested'] = 0
            print(f'Request processed for {user}')
            logging.info(f'Admin has declined deactivation request from {user}')

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
                logging.error('ValueError raised from user input')

        hum_plan.end_date = end
        logging.info(f'Admin has added the following end date for {hum_plan.name}: {end}')
        return hum_plan

    def admin_menu(self):
        continue_admin = True
        while continue_admin:
            choice_format = False
            while not choice_format:
                try:
                    action = int(input('Enter what you would like to do.'
                                       '\n 1 for creating, editing, displaying or ending a humanitarian plan'
                                       '\n 2 for creating, editing, deactivating, reactivating or deleting a volunteer account'
                                       '\n 3 for allocating resources'
                                       '\n 0 to log out and quit the application'))
                    if action in range(0, 4):
                        choice_format = True
                        if action == 0:
                            continue_admin = False
                            exit("You have logged out and quit the application.")
                    else:
                        print('Please enter an integer from 0-3.')
                except ValueError:
                    print('Please enter an integer from 0-3.')
                    logging.error('ValueError raised from user input')
            func_format = False
            while func_format == False:
                if action == 1:
                    try:
                        func = int(input('Enter what you would like to do.'
                                         '\n 1 for creating a humanitarian plan'
                                         '\n 2 for editing a humanitarian plan'
                                         '\n 3 for displaying a humanitarian plan'
                                         '\n 4 for ending a humanitarian plan'))
                        if func in range(1, 5):
                            func_format = True
                            if func == 1:
                                humanitarian_plan = self.create_hum_plan()
                            elif func == 2:
                                pass  # write function for editing
                            elif func == 3:
                                humani_plan = pd.read_csv('humanitarian_plan.csv')
                                while True:
                                    location = v.string("Enter the location of the humanitarian plan you would like to access.")
                                    if any(humani_plan['location'].str.contains(location)) == True:
                                        mask = humani_plan['location'] == location
                                        loc_plan = humani_plan[mask]
                                    else:
                                        print("Location entered does not match that of any humanitarian plans.")
                                        continue
                                    year = v.integer("Enter the year of the humanitarian plan you would like to access.")
                                    year = str(year)
                                    date_plan = str(loc_plan['start_date'])
                                    if year in date_plan:
                                        plan_name = location + '_' + year
                                        self.display_hum_plan(plan_name)
                                        break
                                    else:
                                        print("Year entered does not match location entered.")
                            elif func == 4:
                                pass  # write function for ending
                        else:
                            print('Please enter an integer from 1-4.')
                    except ValueError:
                        logging.error('ValueError raised from user input')
                        print('Please enter an integer from 1-4.')
                if action == 2:
                    self.check_deactivation_requests()
                    try:
                        func = int(input('Enter what you would like to do.'
                                         '\n 1 for creating a volunteer account'
                                         '\n 2 for editing a volunteer account'
                                         '\n 3 for deactivating/reactivating a volunteer account'
                                         '\n 4 for deleting a volunteer account'))
                        if func in range(1, 5):
                            func_format = True
                            if func == 1:
                                self.create_volunteer()
                            elif func == 2:
                                self.edit_volunteer()
                            elif func == 3:
                                self.active_volunteer()
                            elif func == 4:
                                self.delete_volunteer()
                        else:
                            print('Please enter an integer from 1-4.')
                    except ValueError:
                        logging.error('ValueError raised from user input')
                        print('Please enter an integer from 1-4.')
                if action == 3:
                    func_format = True

                    pass

# admin username and password have been hardcoded here
# login process
# admin_authorised = False
# while admin_authorised == False:
#     username_attempt = input("Enter username.")
#     password_attempt = input("Enter password.")
#     if username_attempt == 'admin' and password_attempt == '111':
#         admin_authorised = True
#         try:
#             admin = Admin('admin', '111')
#         except ValueError as e:
#             print(e)  # If login details are incorrect, admin user will not be created
#         else:
#             print(admin)
#             # list of functions for admin to choose what to do, exception handling to ensure correct format
#             admin.admin_menu()
#     else:
#         print("Wrong username or password entered.")




