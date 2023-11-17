import pandas as pd, numpy as np
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
                status = 1    #input this into the csv
                request = 0
                _str = "reactivate"
                break
            elif status == "D":
                status = 0
                _str = "deactivate"
                request = 0
                break

        df = pd.read_csv('users.csv', dtype={'password': str})
        # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
        print(df.iloc[1:, 0])
        while True:
            user = v.string(f'Please enter the username you would like to {_str}. ')
            if any(df['username'].str.contains(user)) == False:  # testing if volunteer account already exists
                print("Username not found. Please enter again.")
            else:
                break
        df.loc[df['username'] == user, 'deactivation_requested'] = request  # modify the dataform
        df.loc[df['username'] == user, 'active'] = status
        df.to_csv('users.csv', index=False)  # write it into the .csv file

        # update files for camps and volunteering sessions
        # users = pd.read_csv('users.csv', dtype={'password': str})
        cur_user = df[df['username'] == user]
        cur_user = cur_user.replace({np.nan: None})
        camp_name = cur_user.iloc[0]['camp_name']
        # increment or decrement number of volunteers if user has a camp
        if camp_name:
            plan_id = cur_user.iloc[0]['plan_id']
            camps = pd.read_csv(plan_id + '.csv')
            user_camp = (camps['camp_name'] == camp_name)
            if status == 1:
                camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] + 1
                camps.to_csv(plan_id + '.csv', index=False)
            if status == 0:
                camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
                camps.to_csv(plan_id + '.csv', index=False)
                # if deactivated: delete the user's volunteering sessions
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times = vol_times.drop(vol_times[vol_times['username'] == user].index)
                vol_times.to_csv('volunteering_times.csv', index=False)


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

            # decrement number of volunteers in camps file if user has a camp
            users = pd.read_csv('users.csv', dtype={'password': str})
            cur_user = users[users['username'] == user]
            cur_user = cur_user.replace({np.nan: None})
            camp_name = cur_user.iloc[0]['camp_name']
            if camp_name:
                plan_id = cur_user.iloc[0]['plan_id']
                camps = pd.read_csv(plan_id + '.csv')
                user_camp = (camps['camp_name'] == camp_name)
                camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
                camps.to_csv(plan_id + '.csv', index=False)
                # delete the user's volunteering sessions
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times = vol_times.drop(vol_times[vol_times['username'] == user].index)
                vol_times.to_csv('volunteering_times.csv', index=False)

        # admin chose to keep account active
        else:
            df.loc[df['username'] == user, 'deactivation_requested'] = 0
            print(f'Request processed for {user}')
            logging.info(f'Admin has declined deactivation request from {user}')

    def allocate(self):
        try:  # first, get the plan which the admin wants to allocate resources to, by entering index
            hum_df = pd.read_csv('humanitarian_plan.csv')
            print(hum_df.iloc[0:])
            index = v.integer(
                "Please enter the index of the humanitarian plan which you would like to allocate resources to.")
            # use the index to pick up the corresponding csv automatically
            start_year = hum_df.loc[index, 'start_date'].split('-')[2]
            location = hum_df.loc[index, 'location'].replace(' ', '_')
            plan_csv = f"{location}_{start_year}.csv"
            print(f"opening {plan_csv}...\n")
        except IndexError:
            print("Please enter a correct index.")

        # show the storage resources
        print(f"This is our total resources ready for distributing.")
        storage_df = pd.read_csv("Storage.csv")
        print(storage_df.to_string(index=False))
        print("")

        # and then show the plan's resources
        print(f"This is the resources details of {location}_{start_year}.")
        plan_df = pd.read_csv(plan_csv)
        print(plan_df.iloc[0:])

        # select the specific camp by entering the index
        camp = v.integer("Please enter the index of the camp where you would like to allocate resources to.\n"
                         "'auto' for auto-allocation.\n")
        camp_name = plan_df.loc[camp, 'camp_name']
        print(f"You have selected {camp_name}.")

        # getting the specific amount of food, water, and medical supplies
        resource = v.string(
            "Please enter the amount of food, water, and medical supplies you would like to distribute,\n"
            "with coma as a separator ('20,30,40, for example):\n").split(",")
        food, water, medical_supplies = resource
        # confirm before sending resource
        confirm = v.string(
            f"You are going to distribute {food} food, {water} water, and {medical_supplies} medical supplies to {camp_name}.\n"
            f"Is that correct? Y/N ")
        # add the resources to the camp
        if confirm == "Y":
            # add and write into the new values
            plan_df.loc[plan_df['camp_name'] == camp_name, 'food'] += int(food)  # like a = a + food
            plan_df.loc[plan_df['camp_name'] == camp_name, 'water'] += int(water)
            plan_df.loc[plan_df['camp_name'] == camp_name, 'medical_supplies'] += int(medical_supplies)
            plan_df.to_csv(plan_csv, index=False)
            print(f"This is the new amount resources in {camp_name}")
            print(plan_df.loc[camp])

            storage_df['food'] -= int(food)
            storage_df['water'] -= int(water)
            storage_df['medical_supplies'] -= int(medical_supplies)
            storage_df.to_csv("Storage.csv", index=False)
            print("This is the remaining resources in storage.\n",
                  storage_df)

        elif confirm == "N":
            ...

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

        # update csv files: add end date; remove volunteer accounts and volunteering sessions for that plan
        plans = pd.read_csv('humanitarian_plan.csv')
        cur_plan = (plans['location'] == hum_plan.location) & (plans['start_date'] == hum_plan.start_date)
        plans.loc[cur_plan, 'end_date'] = end
        plans.to_csv('humanitarian_plan.csv', index=False)

        plan_id = hum_plan.location + "_" + hum_plan.start_date[6:]
        users = pd.read_csv('users.csv', dtype={'password': str})
        users = users.drop(users[users['plan_id'] == plan_id].index)
        users.to_csv('users.csv', index=False)

        vol_times = pd.read_csv("volunteering_times.csv")
        vol_times = vol_times.drop(vol_times[vol_times['plan_id'] == plan_id].index)
        vol_times.to_csv('volunteering_times.csv', index=False)

        return hum_plan

    def display_resources(self, hum_plan):
        """
        This method requires a HumanitarianPlan object as argument
        and prints out the corresponding resources .csv file.
        """
        resources = pd.read_csv('%s_resources.csv' % (hum_plan))
        print(resources)

    def allocate_resources(self, hum_plan):
        """
        This method requires a HumanitarianPlan object as argument, retrieves the
        corresponding resources .csv file and allows admin to allocate resources
        (Food packs, Water or First-Aid Kits) to camps in that HumanitarianPlan from storage.
        """
        resources = pd.read_csv(f"{hum_plan}_resources.csv")
        print(f"Currently, the resources in {hum_plan} are as follows:"
              f"\n{resources}")
        camp_format = False
        while camp_format == False:
            try:
                camp_no = int(input('Enter the camp ID you would like to allocate resources to (only the number).'))
                if any(resources['Location'].str.contains(f"Camp {camp_no}")) == True:
                    camp_format = True
                else:
                    print('The camp ID you entered does not belong to any existing camp in this humanitarian plan.')
            except ValueError:
                logging.error('ValueError raised from user input')
                print('Please enter an integer.')
        camp_index = resources.index[resources['Location'] == f"Camp {camp_no}"]
        print(camp_index)
        choice_format = False
        while choice_format == False:
            try:
                resource_choice = int(input('Enter what resource you would like to allocate.'
                                      '\n 1 for food packs.'
                                      '\n 2 for water.'
                                      '\n 3 for first-aid kits.'))
                if resource_choice in range(1,4):
                    choice_format = True
                else:
                    print('Please enter an integer from 1-3.')
            except ValueError:
                logging.error('ValueError raised from user input')
                print('Please enter an integer from 1-3.')
        if resource_choice == 1: #need to make sure number of {resource} entered does not exceed number in storage
            amount = v.integer(f'Enter the number of food packs you would like to allocate to Camp {camp_no}.')
            amount = int(amount) #please don't remove, error otherwise
            original = resources.loc[0, 'Food Packs']
            new = original - amount
            resources.loc[0, 'Food Packs'] = new
            original = resources.loc[camp_index, 'Food Packs']
            new = original + amount
            resources.loc[camp_index, 'Food Packs'] = new
        elif resource_choice == 2:
            amount = v.integer(f'Enter the number of boxes of water you would like to allocate to Camp {camp_no}.')
            amount = int(amount)  # please don't remove, error otherwise
            original = resources.loc[0, 'Water']
            new = original - amount
            resources.loc[0, 'Water'] = new
            original = resources.loc[camp_index, 'Water']
            new = original + amount
            resources.loc[camp_index, 'Water'] = new
        elif resource_choice == 3:
            amount = v.integer(f'Enter the number of first-aid kits you would like to allocate to Camp {camp_no}.')
            amount = int(amount)  # please don't remove, error otherwise
            original = resources.loc[0, 'First-Aid Kits']
            new = original - amount
            resources.loc[0, 'First-Aid Kits'] = new
            original = resources.loc[camp_index, 'First-Aid Kits']
            new = original + amount
            resources.loc[camp_index, 'First-Aid Kits'] = new
        resources.to_csv(f"{hum_plan}_resources.csv")
        print(f"Allocation complete. Currently, the resources in {hum_plan} are as follows:"
              f"\n{resources}")

    def admin_menu(self):
        continue_admin = True
        while continue_admin:
            choice_format = False
            while not choice_format:
                try:
                    action = int(input('Enter what you would like to do.'
                                       '\n 1 for creating, editing, displaying or ending a humanitarian plan'
                                       '\n 2 for creating, editing, deactivating, reactivating or deleting a volunteer account'
                                       '\n 3 for displaying or allocating resources'
                                       '\n 0 to log out and quit the application'))
                    if action in range(0, 4):
                        choice_format = True
                        if action == 0:
                            continue_admin = False
                            exit("You have logged out and quit the application.")
                        if action == 3:
                            admin.allocate()
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
                                        loc_plan = humani_plan[humani_plan['location'] == location]
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
                    try:
                        func = int(input('Enter what you would like to do.'
                                         '\n 1 for displaying resources in a humanitarian plan.'
                                         '\n 2 for allocating resources to camps.'))
                        if func in range(1,3):
                            func_format = True
                            if func == 1:
                                humani_plan = pd.read_csv('humanitarian_plan.csv')
                                while True:
                                    location = v.string(
                                        "Enter the location of the humanitarian plan you would like to access.")
                                    if any(humani_plan['location'].str.contains(location)) == True:
                                        loc_plan = humani_plan[humani_plan['location'] == location]
                                    else:
                                        print("Location entered does not match that of any humanitarian plans.")
                                        continue
                                    year = v.integer(
                                        "Enter the year of the humanitarian plan you would like to access.")
                                    year = str(year)
                                    date_plan = str(loc_plan['start_date'])
                                    if year in date_plan:
                                        plan_name = location + '_' + year
                                        self.display_resources(plan_name)
                                        break
                                    else:
                                        print("Year entered does not match location entered.")
                            elif func == 2:
                                humani_plan = pd.read_csv('humanitarian_plan.csv')
                                while True:
                                    location = v.string(
                                        "Enter the location of the humanitarian plan you would like to access.")
                                    if any(humani_plan['location'].str.contains(location)) == True:
                                        loc_plan = humani_plan[humani_plan['location'] == location]
                                    else:
                                        print("Location entered does not match that of any humanitarian plans.")
                                        continue
                                    year = v.integer(
                                        "Enter the year of the humanitarian plan you would like to access.")
                                    year = str(year)
                                    date_plan = str(loc_plan['start_date'])
                                    if year in date_plan:
                                        plan_name = location + '_' + year
                                        self.allocate_resources(plan_name)
                                        break
                                    else:
                                        print("Year entered does not match location entered.")
                        else:
                            print('Please enter an integer from 1-2.')
                    except ValueError:
                        logging.error('ValueError raised from user input')
                        print('Please enter an integer from 1-2.')

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




