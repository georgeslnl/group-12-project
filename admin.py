import pandas as pd, numpy as np
from datetime import datetime
from humanitarianplan import HumanitarianPlan
from coded_vars import convert_gender, convert_medical_condition
from selection import select_plan, select_camp, select_camp2, select_plan_camp_vol, select_plan_camp_vol_none
import refugee_profile_funcs, volunteering_session_funcs
import verify as v
import logging


class Admin:
    """Class for the Admin user. Since there can only be 1 admin, this class can only be initialised once"""

    def __init__(self, username, password):
        self.username = username  # if login credentials are correct, admin object is initialised
        self.password = password
        self.logged_in = True
        pd.set_option('display.max_columns', None) #all columns of DataFrames will be displayed (nothing is cut off)

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
        name = f'{loc}_{start_date[6:]}'

        # Opens the csv file and adds the data for this humanitarian plan
        h = open("humanitarian_plan.csv", "a")
        h.write(f'\n{name},{desc},{loc},{start_date},{nb_of_camps},,{1000},{1000},{250}') # default amount of resources
        # desc is wrapped in "" because we don't want to csv file to see a "," in the description as a delimitter
        h.close()

        # Prints out the information about the Humanitarian Plan created
        print(f'A new humanitarian plan has been created with the following information:'
              f'\n\t Description: {desc}'
              f'\n\t Location affected: {loc}'
              f'\n\t Start of the event: {start_date}'
              f'\n\t Number of camps: {nb_of_camps}')

        return hu_pl

    # def display_hum_plan(self, hum_plan):
    #     """
    #     This method displays summary information about the humanitarian plan.
    #     Information to display:
    #         - Number of refugees
    #         - Their camp identification
    #         - Number of volunteers working at each camp
    #     """
    #     hu_pl = pd.read_csv('%s.csv' %(hum_plan))
    #     print('Total number of refugees: ', sum(hu_pl['refugees']))
    #     print('Camp ID of camps involved: \n', hu_pl['camp_name'])
    #     print('Number of volunteers working at each camp: \n', hu_pl[['camp_name', 'volunteers']])

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
        first_name = v.name("Please enter the first name: ")
        last_name = v.name("Please enter the last name: ")
        email = v.email("PLease enter the email address: ")
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

    def end_event(self):
        """
        The method adds the end_date of the selected humanitarian plan.

        The while loop is used to ensure the user inputs a date in the correct format
        """
        plans = pd.read_csv('humanitarian_plan.csv')
        plans = plans[plans['end_date'].isna()]
        print("\nEnd humanitarian plan")
        if len(plans.index) == 0:
            print("There are no ongoing humanitarian plans.")
            return

        print("The following humanitarian plans are ongoing:")
        print("Number - Location - Start Date")
        for row in range(len(plans.index)):
            print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], sep=" - ")

        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                plan_num = int(input("Enter the number of the plan you would like to close: "))
                if plan_num == 0:
                    return
                if plan_num not in range(1, len(plans.index) + 1):
                    raise ValueError
            except ValueError:
                print("Please enter a plan number corresponding to a humanitarian plan listed above.")
                continue

            # enter end date
            while True:
                print("\nEnter [0] to go back to the previous step.")
                end_date = input('Please input the end date of the event (DD-MM-YYYY): ')
                if end_date == "0":
                    break
                try:
                    end = datetime.strptime(end_date, "%d-%m-%Y").date()
                except ValueError:
                    print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 15-12-2023).")
                    logging.error('ValueError raised from user input')
                    continue
                t = datetime.now().date()
                if end > t:
                    print("End date cannot be in the future. Please try again.")
                    continue
                break
            if end_date == "0": # return to plan selection
                continue
            break

        # update csv files: add end date; remove volunteer accounts and volunteering sessions for that plan
        plans = pd.read_csv('humanitarian_plan.csv')
        plans = plans.replace({np.nan: None})
        plans.loc[plan_num-1, 'end_date'] = end_date
        plan_id = plans['plan_id'].iloc[plan_num-1]
        plans.to_csv('humanitarian_plan.csv', index=False)

        users = pd.read_csv('users.csv', dtype={'password': str})
        users = users.drop(users[users['plan_id'] == plan_id].index)
        users.to_csv('users.csv', index=False)

        vol_times = pd.read_csv("volunteering_times.csv")
        vol_times = vol_times.drop(vol_times[vol_times['plan_id'] == plan_id].index)
        vol_times.to_csv('volunteering_times.csv', index=False)

        print("The humanitarian plan", plan_id, "has been closed, with end date", end_date + ".")
        return

    def display_resources(self, hum_plan):
        """
        This method requires a HumanitarianPlan object as argument
        and prints out the corresponding resources .csv file.
        """
        resources = pd.read_csv(hum_plan)
        print(resources)

    def allocate_resources(self, hum_plan, location):
        """
        This method requires a HumanitarianPlan object as argument, retrieves the
        corresponding resources .csv file and allows admin to allocate resources
        (Food packs, Water or First-Aid Kits) to camps in that HumanitarianPlan from storage.
        """
        resources = pd.read_csv(hum_plan)
        humani_plan = pd.read_csv("humanitarian_plan.csv")
        print(f"Currently, the resources in storage as follows:"
              f"\n{humani_plan.loc[humani_plan.location == location,['location','start_date','food_storage','water_storage','firstaid_kits_storage']]}\n")
        print(f"And the resources in {hum_plan[:-4]} are as follows:"
              f"\n{resources}")
        camp_format = False
        while camp_format == False:
            try:
                camp_no = input('Enter the camp ID you would like to allocate resources to (only the number).\n'
                                    'Enter "auto" for auto-allocating resources to all camps for their following 7 days')
                if camp_no.lower() == "auto":
                    # first we count how many resources we need
                    sum_needed = [0, 0, 0]  # food, water, firstaid_kits
                    for i in resources.index:
                        refugees = resources.loc[i, "refugees"]
                        food_needed = refugees * 7 - resources.loc[i, "food"]
                        if food_needed < 0:  # if we have more than 7 days, no need to top-up
                            food_needed = 0
                        sum_needed[0] += food_needed
                        water_needed = refugees * 7 - resources.loc[i, "water"]
                        if water_needed < 0:
                            water_needed = 0
                        sum_needed[1] += water_needed
                        # each person consumes 1/3 kit per day (presumably)
                        firstaid_needed = int((refugees * 7) / 3) - resources.loc[i, "firstaid_kits"]
                        if firstaid_needed < 0:
                            firstaid_needed = 0
                        sum_needed[2] += firstaid_needed

                    # check if we have enough resources in store.
                    food_in_storage = int(humani_plan.loc[humani_plan.location == location, 'food_storage'].iloc[0])
                    # add .iloc[0] at the end if needed to get one single value
                    water_in_storage = int(
                        humani_plan.loc[humani_plan['location'] == location, 'water_storage'].iloc[0])
                    firstaid_in_storage = int(
                        humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'].iloc[0])
                    # if storage resources insufficient
                    if food_in_storage < sum_needed[0] or water_in_storage < sum_needed[1] or firstaid_in_storage < \
                            sum_needed[2]:
                        print("Resources insufficient, please enter manually or request new resources.")
                        camp_format = False

                    # now we add and write one by one, if resources sufficient
                    else:
                        while True:
                            confirm = input(f"{sum_needed[0]} of food, {sum_needed[1]} of water, "
                                            f"and {sum_needed[2]} of first-aid kits will be added to camps from storage.\n"
                                            f"Would you like to proceed? (Y/N)").capitalize()
                            if confirm == "Y":
                                for i in resources.index:
                                    refugees = resources.loc[i, "refugees"]
                                    # food
                                    food_needed = refugees * 7 - resources.loc[i, "food"]
                                    humani_plan.loc[humani_plan['location'] == location, 'food_storage'] -= food_needed
                                    resources.loc[i, "food"] += food_needed
                                    # water
                                    water_needed = refugees * 7 - resources.loc[i, "water"]
                                    humani_plan.loc[
                                        humani_plan['location'] == location, 'water_storage'] -= water_needed
                                    resources.loc[i, "water"] += water_needed
                                    # first-aid
                                    firstaid_needed = int((refugees * 7) / 3) - resources.loc[i, "firstaid_kits"]
                                    humani_plan.loc[
                                        humani_plan['location'] == location, 'firstaid_kits_storage'] -= firstaid_needed
                                    resources.loc[i, "firstaid_kits"] += firstaid_needed
                                    # write each iterate into two .csv
                                    resources.to_csv(hum_plan, index=False)
                                    humani_plan.to_csv("humanitarian_plan.csv", index=False)
                                print(f"\nAllocation complete. Currently, the resources in {hum_plan[:-4]} are as follows:"
                                        f"\n{resources}")
                                print(f"\nAnd the remaining resources in storage: "
                                      f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
                                exit()  # TODO use something else
                            elif confirm == "N":
                                ...  # TODO sort out later
                            else:
                                print("Please enter the correct input (Y/N)")
                elif any(resources['camp_name'].str.contains(f"Camp {camp_no}")):
                    camp_format = True
                else:
                    print('The camp ID you entered does not belong to any existing camp in this humanitarian plan.')
            except ValueError:
                logging.error('ValueError raised from user input')
                print('Please enter an integer.')

        camp_index = resources.index[resources['camp_name'] == f"Camp {camp_no}"]
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

        if resource_choice == 1:
            while True:
                amount = v.integer(f'Enter the number of food packs you would like to allocate to Camp {camp_no}.')
                # making sure number of {resource} entered does not exceed number in storage
                in_storage = humani_plan.loc[humani_plan['location'] == location, 'food_storage']
                if any(in_storage - amount <= 0):
                    print('The amount entered exceeds the amount available in storage.'
                          '\nPlease check the amount in storage and try again.')
                else:
                    humani_plan.loc[humani_plan['location'] == location, 'food_storage'] -= int(amount)
                    resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'food'] += int(amount)# like a = a + food
                    break
        elif resource_choice == 2:
            while True:
                amount = v.integer(f'Enter the number of boxes of water you would like to allocate to Camp {camp_no}.')
                in_storage = humani_plan.loc[humani_plan['location'] == location, 'water_storage']
                if any(in_storage - amount <= 0):
                    print('The amount entered exceeds the amount available in storage.'
                          '\nPlease check the amount in storage and try again.')
                else:
                    humani_plan.loc[humani_plan['location'] == location, 'water_storage'] -= int(amount)
                    resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'water'] += int(amount)  # like a = a + food
                    break
        elif resource_choice == 3:
            while True:
                amount = v.integer(f'Enter the number of first-aid kits you would like to allocate to Camp {camp_no}.')
                in_storage = humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage']
                if any(in_storage - amount <= 0):
                    print('The amount entered exceeds the amount available in storage.'
                          '\nPlease check the amount in storage and try again.')
                else:
                    humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'] -= int(amount)
                    resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'firstaid_kits'] += int(amount)  # like a = a + food
                    break

        resources.to_csv(hum_plan, index=False)
        humani_plan.to_csv("humanitarian_plan.csv", index=False)
        print(f"Allocation complete. Currently, the resources in {hum_plan[:-4]} are as follows:"
              f"\n{resources}")
        print(f"And the remaining resources in storage: "
              f"\n{humani_plan}")

    def admin_menu(self):
        while self.logged_in:
            print("\n---------------")
            print("Admin Menu")
            print("---------------")
            while True:
                print("Choose would you would like to do.")
                print("Enter [1] to create, display, edit or end a humanitarian plan")
                print("Enter [2] to manage volunteer accounts (including camp identification)")
                print("Enter [3] to display or allocate resources")
                print("Enter [4] to manage refugee profiles")
                print("Enter [5] to manage volunteering sessions")
                print("Enter [0] to logout")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(6):
                        logging.error(f"Value error raised - Admin entered {option}")
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has chosen to logout.")
                self.logout()
            if option == 1:
                logging.debug(f"Admin has selected the humanitarian plan menu.")
                self.hum_plan_menu()
            if option == 2:
                logging.debug(f"Admin has selected the volunteer accounts menu.")
                self.vol_accounts_menu()
            if option == 3:
                logging.debug(f"Admin has selected the resources menu.")
                self.resources_menu()
            if option == 4:
                logging.debug(f"Admin has selected the refugee menu.")
                self.refugee_menu()
            if option == 5:
                logging.debug(f"{self.username} has selected the volunteering session menu.")
                self.volunteering_session_menu()

    def hum_plan_menu(self):
        while True:
            print("\nHumanitarian Plans")
            while True:
                print("Enter [1] to create a humanitarian plan")
                print("Enter [2] to display a humanitarian plan")
                print("Enter [3] to edit a humanitarian plan")
                print("Enter [4] to end a humanitarian plan")
                print("Enter [0] to return to the admin menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    logging.debug(f'Admin has entered {user_input}.')
                    if option not in range(5):
                        logging.error(f"Admin has entered {user_input}, raising a ValueError.")
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f"Admin has chosen to create a humanitarian plan.")
                humanitarian_plan = self.create_hum_plan()
            if option == 2:
                logging.debug(f"Admin has chosen to display a humanitarian plan.")
                self.display_plan()
            if option == 3:
                logging.debug(f"Admin has chosen to edit a humanitarian plan.")
                # TODO: add function
            if option == 4:
                logging.debug(f"Admin has chosen to end a humanitarian plan.")
                self.end_event()

    def vol_accounts_menu(self):
        while True:
            print("\nManage Volunteer Accounts")
            while True:
                print("Enter [1] to create a volunteer account")
                print("Enter [2] to view a volunteer's details")
                print("Enter [3] to edit a volunteer's details")
                print("Enter [4] to update a volunteer's camp identification")
                print("Enter [5] to deactivate or reactivate a volunteer account")
                print("Enter [6] to delete a volunteer account")
                print("Enter [0] to return to the admin menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    logging.debug(f'Admin has entered {user_input}.')
                    if option not in range(7):
                        logging.error(f"Admin has entered {user_input}, raising a ValueError.")
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f"Admin has chosen to create a volunteer account.")
                self.create_volunteer()
            if option == 2:
                logging.debug(f"Admin has chosen to view a volunteer's details.")
                self.view_volunteer()
            if option == 3:
                logging.debug(f"Admin has chosen to edit a volunteer's details.")
                self.edit_volunteer()
            if option == 4:
                logging.debug(f"Admin has chosen to edit a volunteer's camp identification.")
                self.update_volunteer_camp()
            if option == 5:
                logging.debug(f"Admin has chosen to deactivate or reactivate a volunteer account.")
                self.active_volunteer()
            if option == 6:
                logging.debug(f"Admin has chosen to delete a volunteer account.")
                self.delete_volunteer()

    def resources_menu(self):
        while True:
            print("\nManage Resources")
            while True:
                print("Enter [1] to display resources for a humanitarian plan")
                print("Enter [2] to allocate resources to camps in a humanitarian plan")
                print("Enter [0] to return to the admin menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    logging.debug(f'Admin has entered {user_input}.')
                    if option not in range(3):
                        logging.error(f"Admin has entered {user_input}, raising a ValueError.")
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f"Admin has chosen to display resources.")
                humani_plan = pd.read_csv('humanitarian_plan.csv')
                while True:
                     try:
                         print(humani_plan)
                         index = v.integer(
                             "Please enter the index of the humanitarian plan of which you would like to display resources.")
                         location = humani_plan.loc[index, 'location'].replace(' ', '_')
                         year = humani_plan.loc[index,'start_date'].split('-')[2]
                         plan_csv = f"{location}_{year}.csv"
                         print(f"\nopening {plan_csv}...\n")
                         self.display_resources(plan_csv)
                         break
                     except KeyError:
                         print("Please enter a correct index.")
            if option == 2:
                logging.debug(f"Admin has chosen to allocate resources.")
                humani_plan = pd.read_csv('humanitarian_plan.csv')
                while True:
                    try:
                        print(humani_plan)
                        index = v.integer(
                            "Please enter the index of the humanitarian plan which you would like to allocate resources to.")
                        location = humani_plan.loc[index, 'location'].replace(' ', '_')
                        year = humani_plan.loc[index, 'start_date'].split('-')[2]
                        hum_plan = f"{location}_{year}.csv"
                        print(f"\nopening {hum_plan}...\n")
                        break
                    except KeyError:
                        print("Please enter a correct index.")
                self.allocate_resources(hum_plan, location)

    def refugee_menu(self):
        while True:
            print("\nManage Refugee Profiles")
            while True:
                print("Enter [1] to create a new refugee profile")
                print("Enter [2] to view a refugee profile")
                print("Enter [3] to edit or remove a refugee profile")
                print("Enter [0] to return to the admin menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(4):
                        logging.error(f'Admin did not select a valid option at the Refugee Profile menu.')
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f'Admin will be taken to the create refugee profile function.')
                self.create_refugee_profile()
            if option == 2:
                logging.debug(f'Admin will be taken to the view refugee profile function.')
                self.view_refugee_profile()
            if option == 3:
                logging.debug(f'Admin will be taken to the edit refugee profile function.')
                self.edit_refugee_profile()

    def volunteering_session_menu(self):
        while True:
            print("\nManage Volunteering Times")
            while True:
                print("Enter [1] to add a volunteering session")
                print("Enter [2] to view a volunteer's volunteering sessions")
                print("Enter [3] to remove a volunteering session")
                print("Enter [0] to return to the admin menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    if option not in range(4):
                        logging.error(f'Admin has entered {user_input}, which raised a ValueError.')
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f'Admin has chosen to return to the volunteer menu.')
                return
            if option == 1:
                logging.debug(f'Admin has chosen to add a volunteering session.')
                self.add_volunteering_session()
            if option == 2:
                logging.debug(f"Admin has chosen to view a volunteer's volunteering sessions.")
                self.view_volunteering_sessions()
            if option == 3:
                logging.debug(f'Admin has chosen to remove a volunteering session.')
                self.remove_volunteering_session()

    def logout(self):
        logging.info(f'Admin has logged out of their session.')
        self.logged_in = False
        print("You are now logged out. See you again!")

    def display_plan(self):
        print("\nDisplay humanitarian plan")
        plans = pd.read_csv('humanitarian_plan.csv')
        if len(plans.index) == 0:
            print("No humanitarian plans have been created.")
            return

        plans = plans.replace({np.nan: None})
        print("Number - Location - Start Date - End Date")
        for row in range(len(plans.index)):
            print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], plans['end_date'].iloc[row],
                  sep=" - ")

        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                plan_num = int(input("Enter the number of the plan you would like to display: "))
                if plan_num == 0:
                    return
                if plan_num not in range(1, len(plans.index) + 1):
                    raise ValueError
            except ValueError:
                print("Please enter a plan number corresponding to a humanitarian plan listed above.")
                continue
            break

        print("\nDetails of humanitarian plan:")
        print("Location:", plans.loc[plan_num - 1, 'location'])
        print("Description:", plans.loc[plan_num - 1, 'description'])
        print("Number of camps:", plans.loc[plan_num - 1, 'number_of_camps'])
        print("Start date:", plans.loc[plan_num - 1, 'start_date'])
        print("End date:", plans.loc[plan_num - 1, 'end_date'])
        print("Food packets in storage:", plans.loc[plan_num - 1, 'food_storage'])
        print("Water portions in storage:", plans.loc[plan_num - 1, 'water_storage'])
        print("First-aid kits in storage:", plans.loc[plan_num - 1, 'firstaid_kits_storage'])

        plan_id = plans.loc[plan_num - 1, 'plan_id']
        camps = pd.read_csv(plan_id + '.csv')
        print("\nCamps in humanitarian plan:")
        print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
        for row in range(len(camps.index)):
            print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                  str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
                  sep=" - ")
        return

    def view_volunteer(self):
        print("\nView volunteer account")
        users = pd.read_csv('users.csv')
        users = users[users['account_type'] == "volunteer"]
        if len(users.index) == 0:
            print("No volunteer accounts have been created.")
            return

        selected = select_plan_camp_vol() # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            username = selected[2]

        select_user = users[users['username'] == username]
        gender_str = convert_gender(select_user.iloc[0]['gender'])
        print("\nDetails of", username, "are as follows:")
        print("Username:", username)
        print("Password:", select_user.iloc[0]['password'])
        print("First name:", select_user.iloc[0]['first_name'])
        print("Last name:", select_user.iloc[0]['last_name'])
        print("Email:", select_user.iloc[0]['email'])
        print("Phone number:", select_user.iloc[0]['phone_number'])
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", select_user.iloc[0]['date_of_birth'])
        print("Plan ID:", select_user.iloc[0]['plan_id'])
        print("Camp name:", select_user.iloc[0]['camp_name'])

        logging.debug(f"{username}'s personal information has been displayed.")
        return

    def update_volunteer_camp(self):
        print("\nUpdate a volunteer's camp identification")
        selected = select_plan_camp_vol_none()  # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            plan_id, camp_name, username = selected

        def add_camp(plan_id):
            camps = pd.read_csv(plan_id + '.csv')
            while True:
                print("\nEnter [X] to return to the previous menu.")
                print("Choose a camp.")
                print("\nCamp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                camp_num = input("Enter the number of the camp the volunteer will join (e.g. [1] for Camp 1): ")
                if camp_num == "X":
                    return None
                try:
                    camp_num = int(camp_num)
                    if camp_num not in range(1, len(camps.index) + 1):
                        raise ValueError
                except ValueError:
                    print("Please enter the number of a camp from the list displayed.")
                    continue
                new_camp = "Camp " + str(camp_num)
                return new_camp

        def edit_camp(plan_id, camp_name):
            camps = pd.read_csv(plan_id + '.csv')
            if len(camps.index) == 1:
                print("There is currently only one camp. It is not possible to change camp identification.")
                return camp_name

            while True:
                print("\nEnter [X] to return to the previous menu.")
                print("Choose a new camp.")
                print("\nCamp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                camp_num = input("Enter the number of the camp the volunteer will join (e.g. [1] for Camp 1): ")
                if camp_num == "X":
                    return camp_name
                try:
                    camp_num = int(camp_num)
                    if camp_num not in range(1, len(camps.index) + 1):
                        raise ValueError
                except ValueError:
                    print("Please enter the number of a camp from the list displayed.")
                    continue
                new_camp = "Camp " + str(camp_num)
                if new_camp == camp_name:
                    print("New camp is the same as current camp. Please try again or return to the previous menu.")
                    continue
                return new_camp

        if not camp_name:
            new_camp = add_camp(plan_id)
        else:
            while True:
                print("Enter [1] to update camp identification")
                print("Enter [2] to remove camp identification")
                print("Enter [0] to return to the previous menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(3):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue

                if option == 0:
                    return
                if option == 1:
                    new_camp = edit_camp(plan_id, camp_name)
                if option == 2:
                    while True:
                        print("\nAre you sure you would like to remove the camp identification of", username + "?")
                        print("All volunteering sessions for this volunteer will be erased.")
                        print("Enter [1] to proceed")
                        print("Enter [0] to go back to the previous step")
                        try:
                            remove_option = int(input("Select an option: "))
                            if remove_option not in (0, 1):
                                raise ValueError
                        except ValueError:
                            print("Please enter a number from the options provided.\n")
                            continue
                        break
                    if remove_option == 0:
                        continue
                    new_camp = None
                break

        # update csv files
        if new_camp != camp_name:
            users = pd.read_csv('users.csv', dtype={'password': str})
            cur_user = (users['username'] == username)
            users.loc[cur_user, 'camp_name'] = new_camp
            users.to_csv('users.csv', index=False)

            camps = pd.read_csv(plan_id + '.csv')
            if new_camp:
                chosen = (camps['camp_name'] == new_camp)
                camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            if camp_name:
                old = (camps['camp_name'] == camp_name)
                camps.loc[old, 'volunteers'] = camps.loc[old, 'volunteers'] - 1
            camps.to_csv(plan_id + '.csv', index=False)

            if camp_name and not new_camp: # remove volunteering sessions
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
                vol_times.to_csv('volunteering_times.csv', index=False)
            if camp_name and new_camp: # change camp_name in volunteering_times.csv
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times.loc[vol_times["username"] == username, "camp_name"] = new_camp
                vol_times.to_csv('volunteering_times.csv', index=False)

            print(username + "'s new camp is:", new_camp)
        return

    def create_refugee_profile(self):
        print("\nAdd refugee profile")

        progress = -2
        # loop allowing user to go back
        while progress < 6:
            if progress == -2:
                plan_id = select_plan()
                if plan_id == 0:
                    return
                else:
                    progress += 1

            if progress == -1:
                camp_name = select_camp2(plan_id)
                if camp_name == "X":
                    return
                elif camp_name == "B":
                    progress -= 1
                else:
                    progress += 1

                camps = pd.read_csv(plan_id + '.csv')
                cur_camp = camps[camps['camp_name'] == camp_name]
                remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']

                if remaining_cap == 0:
                    print("\nYour camp has reached its maximum capacity. Unable to add new refugees.")
                    return
                print("\nYour camp's remaining capacity is " + str(remaining_cap) + ".")
                print("Please return to the previous menu if the refugee's family is larger than this number.")

            if progress == 0:
                refugee_name = refugee_profile_funcs.add_name()
                if refugee_name == "0":
                    return
                elif refugee_name == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 1:
                gender = refugee_profile_funcs.add_gender()
                if gender == 0:
                    return
                elif gender == 9:
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                date_of_birth = refugee_profile_funcs.add_dob()
                if date_of_birth == "0":
                    return
                elif date_of_birth == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                medical_cond = refugee_profile_funcs.add_medical_cond()
                if medical_cond == 0:
                    return
                elif medical_cond == 9:
                    progress -= 1
                else:
                    progress += 1

            elif progress == 4:
                family = refugee_profile_funcs.add_family(remaining_cap)
                if family == "X":
                    return
                elif family == "B":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 5:
                remarks = refugee_profile_funcs.add_remarks()
                if remarks == "0":
                    return
                elif remarks == "9":
                    progress -= 1
                else:
                    progress += 1

        # Update csv tables
        refugees = pd.read_csv('refugees.csv')
        if len(refugees.index) == 0:
            refugee_id = 1
        else:
            refugee_id = refugees['refugee_id'].iloc[-1] + 1
        new_row = {'refugee_id': [refugee_id], 'refugee_name': [refugee_name], 'gender': [gender],
                   'date_of_birth': [date_of_birth], 'plan_id': [plan_id], 'camp_name': [camp_name],
                   'medical_condition': [medical_cond], 'family_members': [family], 'remarks': [remarks]}
        new = pd.DataFrame(new_row)
        refugees = pd.concat([refugees, new], ignore_index=True)
        refugees.to_csv('refugees.csv', index=False)

        camps = pd.read_csv(plan_id + '.csv')
        chosen = (camps['camp_name'] == camp_name)
        camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] + family
        camps.to_csv(plan_id + '.csv', index=False)

        # Print details provided
        gender_str = convert_gender(gender)
        medical_str = convert_medical_condition(medical_cond)

        print("\nRefugee profile created!")
        print("You have entered the following details:")
        print("Refugee name:", refugee_name)
        print("Plan ID:", plan_id)
        print("Camp name:", camp_name)
        print("Gender:", gender_str)
        print("Date of birth:", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        return

    def view_refugee_profile(self):
        print("\nView refugee profile")
        plan_id = select_plan()
        if plan_id == 0:
            return
        camp_name = select_camp(plan_id)
        if camp_name == 0:
            return

        refugees = pd.read_csv('refugees.csv')
        refugees = refugees[(refugees['plan_id'] == plan_id) & (refugees['camp_name'] == camp_name)]
        if len(refugees.index) == 0:
            print("There are no refugees at the selected camp.")
            return

        refugees = refugees.replace({np.nan: None})
        print("You will be prompted for the refugee ID of the refugee whose profile you would like to view.")
        while True:
            print("Enter [1] to proceed")
            print("Enter [2] to list all refugees at the selected camp")
            print("Enter [0] to return to the previous menu")
            try:
                option = int(input("Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 0:
            return
        if option == 2: # list refugees at volunteer's camp
            print("\nRefugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")

        # Obtain refugee ID
        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                refugee_id = int(input("Enter refugee ID: "))
                if refugee_id == 0:
                    return
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("Please enter a refugee ID corresponding to a refugee in your camp.")
                continue
            break

        selected = refugees[refugees['refugee_id'] == refugee_id]
        selected = selected.replace({np.nan: None})
        refugee_name = selected.iloc[0]['refugee_name']
        gender = selected.iloc[0]['gender']
        date_of_birth = selected.iloc[0]['date_of_birth']
        medical_cond = selected.iloc[0]['medical_condition']
        family = selected.iloc[0]['family_members']
        remarks = selected.iloc[0]['remarks']

        gender_str = convert_gender(gender)
        medical_str = convert_medical_condition(medical_cond)

        print("Details of refugee ID:", refugee_id)
        print("Plan ID:", plan_id)
        print("Camp name:", camp_name)
        print("Refugee name:", refugee_name)
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        return

    def edit_refugee_profile(self):
        print("\nEdit or remove refugee profile")
        plan_id = select_plan()
        if plan_id == 0:
            return
        camp_name = select_camp(plan_id)
        if camp_name == 0:
            return

        refugees = pd.read_csv('refugees.csv')
        refugees = refugees[(refugees['plan_id'] == plan_id) & (refugees['camp_name'] == camp_name)]
        if len(refugees.index) == 0:
            print("There are no refugees at the selected camp.")
            return

        refugees = refugees.replace({np.nan: None})
        print("You will be prompted for the refugee ID of the refugee whose profile you would like to edit.")
        while True:
            print("Enter [1] to proceed")
            print("Enter [2] to list all refugees at the selected camp")
            print("Enter [0] to return to the previous menu")
            try:
                option = int(input("Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 0:
            return
        if option == 2: # list refugees at volunteer's camp
            print("\nRefugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")

        # Obtain refugee ID
        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                refugee_id = int(input("Enter refugee ID: "))
                if refugee_id == 0:
                    return
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("Please enter a refugee ID corresponding to a refugee in your camp.")
                continue
            break

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            refugees = pd.read_csv('refugees.csv')
            selected = refugees[refugees['refugee_id'] == refugee_id]
            selected = selected.replace({np.nan: None})
            refugee_name = selected.iloc[0]['refugee_name']
            gender = selected.iloc[0]['gender']
            date_of_birth = selected.iloc[0]['date_of_birth']
            medical_cond = selected.iloc[0]['medical_condition']
            family = selected.iloc[0]['family_members']
            remarks = selected.iloc[0]['remarks']
            # inner loop to catch invalid input
            while True:
                print("\nWhich details would you like to update?")
                print("Enter [1] for refugee name")
                print("Enter [2] for gender")
                print("Enter [3] for date of birth")
                print("Enter [4] for medical condition")
                print("Enter [5] for no. of family members")
                print("Enter [6] for remarks")
                print("Enter [9] to remove the refugee's profile")
                print("Enter [0] to return to the previous menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in (0,1,2,3,4,5,6,9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break

            if option == 0:
                return
            if option == 1:
                refugee_profile_funcs.edit_refugee_name(refugee_id, refugee_name)
            if option == 2:
                refugee_profile_funcs.edit_gender(refugee_id, gender)
            if option == 3:
                refugee_profile_funcs.edit_dob(refugee_id, date_of_birth)
            if option == 4:
                refugee_profile_funcs.edit_medical_cond(refugee_id, medical_cond)
            if option == 5:
                refugee_profile_funcs.edit_family(plan_id, camp_name, refugee_id, family)
            if option == 6:
                refugee_profile_funcs.edit_remarks(refugee_id, remarks)
            if option == 9:
                refugee_profile_funcs.remove_refugee(plan_id, camp_name, refugee_id, refugee_name, family)
                return

    def add_volunteering_session(self):
        print("\nAdd a volunteering session")
        print("Select the volunteer for whom you are adding a session.")
        selected = select_plan_camp_vol()
        if selected == 0:
            return
        else:
            plan_id, camp_name, username = selected

        print("\nAdding a volunteering session for", username + "...")
        vol_times = pd.read_csv("volunteering_times.csv")
        cur_user_times = vol_times[vol_times['username'] == username]
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])

        progress = 0
        # loop allowing user to go back
        while progress < 4:
            if progress == 0:
                vol_date = volunteering_session_funcs.select_date()
                if vol_date == "0":
                    return
                else:
                    progress += 1

            elif progress == 1:
                start_time = volunteering_session_funcs.select_start_time(vol_date, cur_user_times)
                if start_time == "0":
                    return
                elif start_time == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                end_time = volunteering_session_funcs.select_end_time(start_time, cur_user_times)
                if end_time == "X":
                    return
                elif end_time == "B":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                confirm = volunteering_session_funcs.confirm_slot(start_time, end_time)
                if confirm == 0:
                    return
                elif confirm == 9:
                    progress -= 1
                else:
                    progress += 1

        # update csv file
        vol_times = open("volunteering_times.csv", "a")
        vol_times.write(f'\n{username},{plan_id},{camp_name},{start_time},{end_time}')
        vol_times.close()
        print("Volunteering session added successfully!")
        return

    def view_volunteering_sessions(self):
        print("\nView volunteering sessions")
        print("Select the volunteer whose sessions you are viewing.")
        selected = select_plan_camp_vol()
        if selected == 0:
            return
        else:
            username = selected[2]

        vol_times = pd.read_csv("volunteering_times.csv")
        cur_user_times = vol_times[vol_times['username'] == username]
        if len(cur_user_times.index) == 0:
            print(username, "does not have any volunteering sessions.")
            return

        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])
        print(username, "has added the following volunteering sessions:")
        for row in range(len(cur_user_times.index)):
            print(str(row+1) + ".", "Start:", datetime.strptime(cur_user_times['start_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"),
                  "\t", "End:", datetime.strptime(cur_user_times['end_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"))
        return

    def remove_volunteering_session(self):
        print("\nRemove a volunteering session")
        print("Select the volunteer for whom you are removing a session.")
        selected = select_plan_camp_vol()
        if selected == 0:
            return
        else:
            username = selected[2]

        vol_times = pd.read_csv("volunteering_times.csv")
        cur_user_times = vol_times[vol_times['username'] == username]
        if len(cur_user_times.index) == 0:
            print(username, "does not have any volunteering sessions.")
            return
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])

        while True:
            print("\nEnter [X] to return to the previous menu.")
            print(username + "'s volunteering sessions:")
            for row in range(len(cur_user_times.index)):
                start = datetime.strptime(cur_user_times['start_time'].iloc[row], '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
                end = datetime.strptime(cur_user_times['end_time'].iloc[row], '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
                print("[" + str(row + 1) + "]", "Start:", start, "\t", "End:", end)
            remove = input("Enter the number of the session you would like to remove: ").strip()
            if remove == "X":
                return
            try:
                remove = int(remove)
                if remove not in range(1, len(cur_user_times.index) + 1):
                    raise ValueError
            except ValueError:
                print("Please enter a number corresponding to one of the above volunteering sessions.")
                continue

            # confirmation
            start = datetime.strptime(cur_user_times['start_time'].iloc[remove-1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            end = datetime.strptime(cur_user_times['end_time'].iloc[remove-1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            while True:
                print("\nAre you sure you would like to remove the following session?")
                print("Start:", start, "\t", "End:", end)
                print("Enter [1] to proceed")
                print("Enter [0] to go back to the previous step")
                try:
                    remove_option = int(input("Select an option: "))
                    if remove_option not in (0, 1):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break
            if remove_option == 0:
                continue

            # update csv file
            vol_times = vol_times.drop(vol_times[(vol_times['username'] == username) &
                                                 (vol_times['start_time'] == cur_user_times['start_time'].iloc[remove-1])].index)
            vol_times.to_csv('volunteering_times.csv', index=False)
            print("Volunteering session has been removed.")
            return

    # old admin menu
    # def admin_menu(self):
    #     continue_admin = True
    #     while continue_admin:
    #         choice_format = False
    #         while not choice_format:
    #             try:
    #                 action = int(input('Enter what you would like to do.'
    #                                    '\n 1 for creating, editing, displaying or ending a humanitarian plan'
    #                                    '\n 2 for creating, editing, deactivating, reactivating or deleting a volunteer account'
    #                                    '\n 3 for displaying or allocating resources'
    #                                    '\n 0 to log out and quit the application'))
    #                 if action in range(0, 4):
    #                     choice_format = True
    #                     if action == 0:
    #                         continue_admin = False
    #                         exit("You have logged out and quit the application.")
    #                 else:
    #                     print('Please enter an integer from 0-3.')
    #             except ValueError:
    #                 print('Please enter an integer from 0-3.')
    #                 logging.error('ValueError raised from user input')
    #         func_format = False
    #         while func_format == False:
    #             if action == 1:
    #                 try:
    #                     func = int(input('Enter what you would like to do.'
    #                                      '\n 1 for creating a humanitarian plan'
    #                                      '\n 2 for editing a humanitarian plan'
    #                                      '\n 3 for displaying a humanitarian plan'
    #                                      '\n 4 for ending a humanitarian plan'))
    #                     if func in range(1, 5):
    #                         func_format = True
    #                         if func == 1:
    #                             humanitarian_plan = self.create_hum_plan()
    #                         elif func == 2:
    #                             pass  # write function for editing
    #                         elif func == 3:
    #                             humani_plan = pd.read_csv('humanitarian_plan.csv')
    #                             while True:
    #                                 location = v.string("Enter the location of the humanitarian plan you would like to access.")
    #                                 if any(humani_plan['location'].str.contains(location)) == True:
    #                                     loc_plan = humani_plan[humani_plan['location'] == location]
    #                                 else:
    #                                     print("Location entered does not match that of any humanitarian plans.")
    #                                     continue
    #                                 year = v.integer("Enter the year of the humanitarian plan you would like to access.")
    #                                 year = str(year)
    #                                 date_plan = str(loc_plan['start_date'])
    #                                 if year in date_plan:
    #                                     plan_name = location + '_' + year
    #                                     self.display_hum_plan(plan_name)
    #                                     break
    #                                 else:
    #                                     print("Year entered does not match location entered.")
    #                         elif func == 4:
    #                             pass  # write function for ending
    #                     else:
    #                         print('Please enter an integer from 1-4.')
    #                 except ValueError:
    #                     logging.error('ValueError raised from user input')
    #                     print('Please enter an integer from 1-4.')
    #             if action == 2:
    #                 self.check_deactivation_requests()
    #                 try:
    #                     func = int(input('Enter what you would like to do.'
    #                                      '\n 1 for creating a volunteer account'
    #                                      '\n 2 for editing a volunteer account'
    #                                      '\n 3 for deactivating/reactivating a volunteer account'
    #                                      '\n 4 for deleting a volunteer account'))
    #                     if func in range(1, 5):
    #                         func_format = True
    #                         if func == 1:
    #                             self.create_volunteer()
    #                         elif func == 2:
    #                             self.edit_volunteer()
    #                         elif func == 3:
    #                             self.active_volunteer()
    #                         elif func == 4:
    #                             self.delete_volunteer()
    #                     else:
    #                         print('Please enter an integer from 1-4.')
    #                 except ValueError:
    #                     logging.error('ValueError raised from user input')
    #                     print('Please enter an integer from 1-4.')
    #             if action == 3:
    #                 try:
    #                     func = int(input('Enter what you would like to do.'
    #                                      '\n 1 for displaying resources in a humanitarian plan.'
    #                                      '\n 2 for allocating resources to camps.'))
    #                     if func in range(1,3):
    #                         func_format = True
    #                         if func == 1:
    #                             humani_plan = pd.read_csv('humanitarian_plan.csv')
    #                             while True:
    #                                 try:
    #                                     print(humani_plan)
    #                                     index = v.integer(
    #                                         "Please enter the index of the humanitarian plan which you would like to allocate resources to.")
    #                                     location = humani_plan.loc[index, 'location'].replace(' ', '_')
    #                                     year = humani_plan.loc[index,'start_date'].split('-')[2]
    #                                     plan_csv = f"{location}_{year}.csv"
    #                                     print(f"\nopening {plan_csv}...\n")
    #                                     self.display_resources(plan_csv)
    #                                     break
    #                                 except KeyError:
    #                                     print("Please enter a correct index.")
    #
    #                         elif func == 2:
    #                             humani_plan = pd.read_csv('humanitarian_plan.csv')
    #                             while True:
    #                                 try:
    #                                     print(humani_plan)
    #                                     index = v.integer(
    #                                         "Please enter the index of the humanitarian plan §which you would like to allocate resources to.")
    #                                     location = humani_plan.loc[index, 'location'].replace(' ', '_')
    #                                     year = humani_plan.loc[index, 'start_date'].split('-')[2]
    #                                     hum_plan = f"{location}_{year}.csv"
    #                                     print(f"\nopening {hum_plan}...\n")
    #                                     self.allocate_resources(hum_plan, location)
    #                                     break
    #                                 except KeyError:
    #                                     print("Please enter a correct index.")
    #                     else:
    #                         print('Please enter an integer from 1-2.')
    #                 except ValueError:
    #                     logging.error('ValueError raised from user input')
    #                     print('Please enter an integer from 1-2.')
