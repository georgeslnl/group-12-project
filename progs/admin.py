# built-in modules
import pandas as pd, numpy as np, os
from datetime import datetime
import logging
# custom modules and functions from other files
from progs.humanitarianplan import HumanitarianPlan
from progs.coded_vars import convert_gender, convert_medical_condition
from progs.selection import select_plan, select_camp
from progs.selection_volunteer import select_plan_camp_vol
from progs.selection_refugees import select_plan_camp_refugee
from progs import auto_resources, hum_plan_funcs, volunteer_funcs, refugee_profile_funcs, volunteering_session_funcs, resource_consumption
from progs import verify as v


class Admin:
    """Class for the Admin user. Since there can only be 1 admin, this class can only be initialised once"""

    def __init__(self, username, password):
        self.username = username  # if login credentials are correct, admin object is initialised
        self.password = password
        self.logged_in = True
        pd.set_option('display.max_columns', None)  # all columns of DataFrames will be displayed (nothing is cut off)

    def create_hum_plan(self):
        """This method lets the admin create a new humanitarian plan.
           The admin needs to input a description, the location affected, the start date of the event, and the number
           of camps.
           The method then creates a new HumanitarianPlan object, which initialises a csv file for the plan's camps.
           It also adds the Humanitarian Plan to the csv file 'humanitarian_plan.csv'
           """
        print("\n--------------------------------------------")
        print("\tCREATE HUMANITARIAN PLAN")
        progress = 0
        while progress < 4:
            if progress == 0:
                desc = hum_plan_funcs.add_description()
                if desc == "0":
                    logging.debug("Returning to previous menu.")
                    return
                else:
                    progress += 1

            if progress == 1:
                loc = hum_plan_funcs.add_location()
                if loc == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif loc == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            if progress == 2:
                start_date = hum_plan_funcs.add_start_date(loc)
                if start_date == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif start_date == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            if progress == 3:
                nb_of_camps = hum_plan_funcs.add_num_camps()
                if nb_of_camps == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif nb_of_camps == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

        # Creating humanitarian plan object
        logging.debug("Finished entering details of humanitarian plan."
                      "Creating humanitarian plan object, which will create a csv file for the plan's camps.")
        hu_pl = HumanitarianPlan(desc, loc, start_date, nb_of_camps)
        name = f'{loc}_{start_date[6:]}'

        # Opens the csv file and adds the data for this humanitarian plan
        h = open(os.path.join('data', 'humanitarian_plan.csv'), "a")
        h.write(f'\n{name},{desc},{loc},{start_date},{nb_of_camps},,{1000},{1000},{250}')  # default amount of resources
        # desc is wrapped in "" because we don't want to csv file to see a "," in the description as a delimitter
        h.close()

        # sort by plan_id after a new plan is added
        plans = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        plans = plans.sort_values(by=['plan_id'])
        plans.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
        logging.debug("humanitarian_plan.csv updated")

        # Prints out the information about the Humanitarian Plan created
        print(f'A new humanitarian plan has been created with the following information:'
              f'\n\t Description: {desc}'
              f'\n\t Location affected: {loc}'
              f'\n\t Start date of the event: {start_date}'
              f'\n\t Number of camps: {nb_of_camps}')
        return

    def edit_hum_plan(self):
        print("\n--------------------------------------------")
        print("\tEDIT HUMANITARIAN PLAN")
        hum_plan_df = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        hum_plan_df = hum_plan_df[hum_plan_df['end_date'].isna()]
        hum_plan_df = hum_plan_df.reset_index(drop=True)
        if len(hum_plan_df.index) == 0:
            print("There are no ongoing humanitarian plans.")
            logging.warning("No ongoing humanitarian plans. Returning to humanitarian plan menu.")
            return

        progress = 0
        edit_choice = None  # remove red underline under progress == 2
        while progress < 4:
            if progress == 0:
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to previous menu.")
                    return
                progress += 1

            elif progress == 1:
                logging.debug("Admin prompted to select what to edit.")
                while True:
                    print("\nEnter [0] to return to the previous menu or [9] to return to plan selection.")
                    print("Please choose what you would like to edit.")
                    print(f'Enter [1] to change the description of {plan_id}.')
                    print(f'Enter [2] to change the number of camps of {plan_id}.\n')
                    edit_choice = v.integer('>>Select an option: ')
                    if edit_choice in (0, 1, 2, 9):
                        break
                    else:
                        print('\nPlease enter a number from the options provided.')
                        logging.error("Invalid user input.")
                if edit_choice == 0:
                    logging.debug("Returning to previous menu.")
                    return
                elif edit_choice == 9:
                    logging.debug("Returning to previous step.")
                    progress -= 1
                elif edit_choice == 1 or edit_choice == 2:
                    progress += 1

            elif progress == 2:
                if edit_choice == 1:
                    selected = hum_plan_df[hum_plan_df['plan_id'] == plan_id]
                    cur_desc = selected['description'].iloc[0]
                    # cur_desc = str(hum_plan_df.loc[hum_plan_df.index == plan_index, "description"])
                    # cur_desc = cur_desc.split('\n')[0]
                    # cur_desc = cur_desc[5:]
                    print(f'\nYou have chosen to edit the description of {plan_id}.'
                          f'\n The current description is:'
                          f'\n {cur_desc}')
                    # edit_description can update its own copy of the csv files and return the updated description
                    new_desc = hum_plan_funcs.edit_description(plan_id, cur_desc)
                    if new_desc == "0":
                        logging.debug("Returning to previous menu.")
                        return
                    elif new_desc == "9":
                        logging.debug("Returning to previous step.")
                        progress -= 1
                    else:
                        # update hum_plan_df in case other details are updated after this
                        hum_plan_df.loc[hum_plan_df["plan_id"] == plan_id, "description"] = new_desc
                        print('\nThe change has been saved.')
                        progress += 1

                elif edit_choice == 2:
                    selected = hum_plan_df[hum_plan_df['plan_id'] == plan_id]
                    num_camps = selected['number_of_camps'].iloc[0]
                    # num_camps = hum_plan_df.loc[hum_plan_df.index == plan_index, "number_of_camps"]
                    # num_camps = num_camps[5:]
                    print(f'\nYou have chosen to edit the number of camps of {plan_id}.'
                          f'\n The current number of camps is:'
                          f'\n {num_camps}')
                    # edit_no_camps can update its own copies of the csv files and return the updated no. of camps
                    new_num = hum_plan_funcs.edit_no_camps(plan_id, num_camps)
                    if new_num == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    elif new_num == "B":
                        logging.debug("Returning to previous step.")
                        progress -= 1
                    else:
                        # update hum_plan_df in case other details are updated after this
                        hum_plan_df.loc[hum_plan_df["plan_id"] == plan_id, "number_of_camps"] = new_num
                        progress += 1

            elif progress == 3:
                logging.debug("Admin prompted to select what to do next.")
                while True:
                    print(f'\nEnter [1] to edit other details of {plan_id}')
                    print("Enter [2] to edit details of other humanitarian plans")
                    print("Enter [0] to exit the edit humanitarian plan function and return to the previous menu")
                    next = v.integer(">>Select an option: ")
                    if next in range(0, 3):
                        if next == 0:
                            logging.debug("Returning to previous menu.")
                            return
                        elif next == 1:
                            logging.debug("Returning to edit details of the same plan.")
                            progress = 1
                        elif next == 2:
                            logging.debug("Returning to select another plan to edit.")
                            progress = 0
                        break
                    else:
                        print('\nPlease enter a number from the options provided.')
                        logging.error("Invalid user input.")

    def create_volunteer(self):
        """
        Enables the admin to create a volunteer account at a selected humanitarian plan.
        The admin is prompted for the volunteer's details one by one.
        """
        print("\n--------------------------------------------")
        print("\tCREATE VOLUNTEER ACCOUNT")
        print("You will be prompted to enter the volunteer's details.")

        progress = 0
        # loop allowing user to go back
        while progress < 10:
            if progress == 0:
                plan_id = volunteer_funcs.add_plan()
                if plan_id == "X":
                    logging.debug("Returning to previous menu.")
                    return
                else:
                    progress += 1

            elif progress == 1:
                camp_name = volunteer_funcs.add_camp(plan_id)
                if camp_name == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif camp_name == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                username = volunteer_funcs.add_username()
                if username == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif username == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                password = volunteer_funcs.add_password()
                if password == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif password == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 4:
                first_name = volunteer_funcs.add_first_name()
                if first_name == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif first_name == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 5:
                last_name = volunteer_funcs.add_last_name()
                if last_name == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif last_name == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 6:
                gender = volunteer_funcs.add_gender()
                if gender == 0:
                    logging.debug("Returning to previous menu.")
                    return
                elif gender == 9:
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 7:
                date_of_birth = volunteer_funcs.add_dob()
                if date_of_birth == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif date_of_birth == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 8:
                email = volunteer_funcs.add_email()
                if email == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif email == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 9:
                phone_number = volunteer_funcs.add_phone_num()
                if phone_number == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif phone_number == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

        logging.debug("Admin has finished entering volunteer details.")
        # update csv files
        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        new_row = {'username': [username], 'password': [password], 'account_type': ['volunteer'], 'active': [1],
                   'deactivation_requested': [0], 'first_name': [first_name], 'last_name': [last_name],
                   'email': [email], 'phone_number': [phone_number], 'gender': [gender],
                   'date_of_birth': [date_of_birth], 'plan_id': [plan_id], 'camp_name': [camp_name]}
        new = pd.DataFrame(new_row)
        users = pd.concat([users, new], ignore_index=True)
        users = users.sort_values(by=['username'])  # sort by username before saving
        users.to_csv(os.path.join('data', 'users.csv'), index=False)
        logging.debug("users.csv updated")

        if camp_name:
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            chosen = (camps['camp_name'] == camp_name)
            camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
            logging.debug("camps csv file updated")

        # Print details provided in registration
        gender_str = convert_gender(gender)
        print("\n" + username, "has been registered as a volunteer.")
        print("You have entered the following details:")
        print("Plan:", plan_id)
        print("Camp:", camp_name)
        print("Username:", username)
        print("Email:", email)
        print("Phone number:", phone_number)
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", date_of_birth)
        return

    def edit_volunteer(self):
        """
        Enables the admin to edit the personal details of a selected volunteer.
        Once the volunteer is selected, a menu enables the admin to edit multiple details before leaving the method.
        """
        print("\n--------------------------------------------")
        print("\tEDIT VOLUNTEER DETAILS")
        print("Select the volunteer whose details you are updating.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            username = selected[2]

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            select_user = users[users['username'] == username]
            password = select_user.iloc[0]['password']
            first_name = select_user.iloc[0]['first_name']
            last_name = select_user.iloc[0]['last_name']
            gender = select_user.iloc[0]['gender']
            date_of_birth = select_user.iloc[0]['date_of_birth']
            email = select_user.iloc[0]['email']
            phone_number = select_user.iloc[0]['phone_number']

            # inner loop to catch invalid input
            while True:
                logging.debug("Admin prompted to select which detail to edit.")
                print("\nEdit details of", username)
                print("Enter [1] for username")
                print("Enter [2] for password")
                print("Enter [3] for first name")
                print("Enter [4] for last name")
                print("Enter [5] for gender")
                print("Enter [6] for date of birth")
                print("Enter [7] for email")
                print("Enter [8] for phone number")
                print("Enter [0] to return to the previous menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(9):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break

            if option == 0:
                logging.debug("Finished editing volunteer details. Returning to volunteer accounts menu.")
                return
            if option == 1:
                edit_username_result = volunteer_funcs.edit_username(username)
                if edit_username_result != "0":
                    username = edit_username_result
            if option == 2:
                volunteer_funcs.edit_password(username, password)
            if option == 3:
                volunteer_funcs.edit_first_name(username, first_name)
            if option == 4:
                volunteer_funcs.edit_last_name(username, last_name)
            if option == 5:
                volunteer_funcs.edit_gender(username, gender)
            if option == 6:
                volunteer_funcs.edit_dob(username, date_of_birth)
            if option == 7:
                volunteer_funcs.edit_email(username, email)
            if option == 8:
                volunteer_funcs.edit_phone_num(username, phone_number)

    def delete_volunteer(self):
        """
        Enables the admin to delete the account of a selected volunteer.
        The admin is asked for confirmation before the deletion is carried out.
        """
        print("\n--------------------------------------------")
        print("\tDELETE VOLUNTEER ACCOUNT")
        print("Select the volunteer whose account you would like to delete.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            plan_id, camp_name, username = selected

        logging.debug(f"Admin prompted to confirm deletion of {username}'s account.")
        while True:
            print("\nAre you sure you would like to delete the account of", username + "?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the previous menu\n")
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break
        if option == 0:
            logging.debug("Returning to previous menu.")
            return

        logging.debug(f"Admin has deleted {username}'s account.")
        # update csv files
        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        users = users.drop(users[users['username'] == username].index)
        users.to_csv(os.path.join('data', 'users.csv'), index=False)
        logging.debug("users.csv updated")

        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
        vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
        logging.debug("volunteering_times.csv updated")

        if camp_name:
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            user_camp = (camps['camp_name'] == camp_name)
            camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
            camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
            logging.debug("camps csv file updated")

        print(username + "'s account has been deleted successfully.")

    def active_volunteer(self):
        """
        Enables the admin to deactivate or reactivate the account of a selected volunteer.
        If the volunteer's account is currently active, the admin is asked to confirm deactivation.
        If the volunteer's account is currently deactivated, the admin is asked to confirm reactivation.
        """
        print("\n--------------------------------------------")
        print(" DEACTIVATE OR REACTIVATE VOLUNTEER ACCOUNT")
        print("Select the volunteer whose account you would like to deactivate or reactivate.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            plan_id, camp_name, username = selected

        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        select_user = users[users['username'] == username]
        active = select_user.iloc[0]['active']

        logging.debug("Admin prompted to confirm deactivation/reactivation.")
        while True:
            if active:
                status = 0
                change = "deactivate"
                print("\n" + username + "'s account is currently active.")
            else:
                status = 1
                change = "reactivate"
                print("\n" + username + "'s account has been deactivated.")
            print("Proceed to", change, "account?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the previous menu\n")
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break
        if option == 0:
            logging.debug("Returning to previous menu.")
            return

        logging.debug(f"Admin has {change}d {username}'s account.")
        # update csv files
        users.loc[users['username'] == username, 'deactivation_requested'] = 0
        users.loc[users['username'] == username, 'active'] = status
        users.to_csv(os.path.join('data', 'users.csv'), index=False)
        logging.debug("users.csv updated")

        # increment or decrement number of volunteers if user has a camp
        if camp_name:
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            user_camp = (camps['camp_name'] == camp_name)
            if status == 1:
                camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] + 1
                camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
                logging.debug("camps csv file updated")
            if status == 0:
                camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
                camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
                logging.debug("camps csv file updated")
                # if deactivated: delete the user's volunteering sessions
                vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
                vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
                vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
                logging.debug("volunteering_times.csv updated")

        print(username + "'s account has been " + change + "d successfully.")

    def low_resources_notification(self):

        # Getting the plan_id of all the plans created
        humani_plan = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        plans = []
        for index, row in humani_plan.iterrows():
            plans.append(row["plan_id"])

        for plan_id in plans:  # iterate through each humanitarian plan created
            current_plan = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            nb_of_camps = 0  # number of camps with low resources

            for i in current_plan.index:  # iterate through each camp of the current humanitarian plan
                refugees = current_plan.loc[i, "refugees"]
                camp = current_plan.loc[i, "camp_name"]
                food_left = refugees * 2 - current_plan.loc[i, "food"]
                water_left = refugees * 2 - current_plan.loc[i, "water"]
                firstaid_left = auto_resources.med_needed(plan_id, camp)*2 - current_plan.loc[i, "firstaid_kits"]

                # if food_left > 0:  # if there is less than two days' worth of food
                #     print(f'* Warning: {plan_id}\'s {camp} is running low on food. Please navigate to the '
                #           f'resource allocation menu *')
                # if water_left > 0:
                #     print(f'* Warning: {plan_id}\'s {camp} is running low on water. Please navigate to the '
                #           f'resource allocation menu *')
                # if firstaid_left > 0:
                #     print(f'* Warning: {plan_id}\'s {camp} is running low on first-aid kits. Please navigate to the '
                #           f'resource allocation menu *')

                if food_left > 0 or water_left > 0 or firstaid_left > 0:  # if there is less than two days' worth of food
                    nb_of_camps += 1

            if nb_of_camps == 1:
                print(f'* Warning: {plan_id} has {nb_of_camps} camp with low resources. *')
            elif nb_of_camps > 1:
                print(f'* Warning: {plan_id} has {nb_of_camps} camps with low resources. *')
            else:
                logging.debug("No camps with low resources.")
            logging.debug("Finished checking for camps with low resources.")

    def resource_request_notification(self):
        try:
            requests = pd.read_csv(os.path.join('data', 'resource_requests.csv'))
        except FileNotFoundError:
            return False # returns nothing if no new requests
        else:
            # if no new requests have been made, the column 'resolved' should only contain 'yes' values
            nb_of_requests = len(requests[requests["resolved"] == 'no'])
            if nb_of_requests == 0:
                logging.debug("No resource requests.")
                return False # returns nothing if no new requests
            elif nb_of_requests == 1:
                print(f'\n* You have received {nb_of_requests} new request to allocate resources. *')
                return requests
            else:
                print(f'\n* You have received {nb_of_requests} new requests to allocate resources. *')
                return requests

    def resource_request_menu(self):
        """
        This method is called to check requests made by volunteers to allocate resources to their camps.
        The method will iterate through every resource request that isn't resolved.
        This method uses the resource_requests.csv file to check for requests and amount requested.
        """
        logging.debug("Checking for resource requests.")
        requests = self.resource_request_notification()
        if requests is not False:  # if method above didn't return false
            new_requests = requests[requests["resolved"] == 'no']
            for index, row in new_requests.iterrows():
                logging.debug("Processing next request.")
                user = row["username"]
                plan = row["plan_id"]
                camp = row["camp_name"]
                food_request = row["food"]
                water_request = row["water"]
                kit_request = row["firstaid_kits"]

                # Food requests
                logging.debug("Admin prompted to continue to food portion of request.")
                while True:
                    option = v.string("\n>>Enter [C] to continue, or [X] to return to the previous menu: ")
                    if option.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    elif option.upper() == "C":
                        if food_request == 0:
                            print('\nNo requests for food.')
                            break
                        self.resource_request_processing(food_request, 'food', user, camp, plan)
                        break
                    else:
                        print("\nPlease enter either [C] or [X].")
                        logging.error("Invalid user input.")

                # Water requests
                logging.debug("Admin prompted to continue to water portion of request.")
                while True:
                    option = v.string("\n>>Enter [C] to continue, or [X] to return to the previous menu: ")
                    if option.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    elif option.upper() == "C":
                        if water_request == 0:
                            print('\nNo requests for water.')
                            break
                        self.resource_request_processing(water_request, 'water', user, camp, plan)
                        break
                    else:
                        print("\nPlease enter either [C] or [X].")
                        logging.error("Invalid user input.")

                # First-aid kit requests
                logging.debug("Admin prompted to continue to first-aid kit portion of request.")
                while True:
                    option = v.string("\n>>Enter [C] to continue, or [X] to return to the previous menu: ")
                    if option.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    elif option.upper() == "C":
                        if kit_request == 0:
                            print('\nNo requests for first-aid kits.')
                            break
                        self.resource_request_processing(kit_request, 'fofirstaid_kits', user, camp, plan)
                        break
                    else:
                        print("\nPlease enter either [C] or [X]")
                        logging.error("Invalid user input.")

                # Marking that request as resolved
                requests.loc[index, "resolved"] = 'yes'
                logging.debug("Request marked as resolved.")

            # Saves to csv after iterating through all the new requests and marking them as resolved.
            logging.debug("Finished processing resource requests.")
            requests.to_csv(os.path.join('data', 'resource_requests.csv'), index=False)
            logging.debug("resource_requests.csv saved")


    def resource_request_processing(self, requested_nb, resource, user, camp, plan):
        """
        This method is called when a request for more resources has been made by a volunteer.
        The admin uses the method to either accept or decline the request, updating the storage and
        camp resources accordingly.
        """
        resources_df = pd.read_csv(os.path.join('data', plan + '.csv'))
        humani_plan_df = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        if resource != 0:
            print(f'\n{user} has requested {requested_nb} {resource} for {camp} of {plan}\n')
            storage_units = humani_plan_df.loc[humani_plan_df.plan_id == plan, f'{resource}_storage'].item()
            camp_units = resources_df.loc[resources_df.camp_name == camp, resource].item()
            print(f'{plan}\'s {resource} storage units: {storage_units}')
            print(f'{camp}\'s {resource} units: {camp_units}\n')

            if requested_nb > storage_units:
                print('Amount requested is too high, storage units are too low!')
                print('Please add more resources to the storage before proceeding')
                # We could add a call to the add_storage_resource method here once we have it?
                logging.warning(f"Amount of {resource} requested exceeds storage. Unable to approve request.")
                return

            logging.debug(f"Admin prompted to approve or decline request for {resource}.")
            while True:
                print('Enter [1] to approve their request')
                print('Enter [2] to decline their request\n')
                try:
                    option = int(input(">>Select an option: "))
                    if option not in (1, 2):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 1:
                print('\nRequest accepted')
                humani_plan_df.loc[humani_plan_df.plan_id == plan, f'{resource}_storage'] -= requested_nb
                humani_plan_df.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
                resources_df.loc[resources_df.camp_name == camp, resource] += requested_nb
                resources_df.to_csv(os.path.join('data', plan + '.csv'), index=False)
                print(f'The {resource} units for {camp} have increased by: {requested_nb}')
                print('This request has been marked as resolved.')
                logging.debug("Request approved. humanitarian_plan.csv and camps csv file updated.")
            elif option == 2:
                print('\nRequest declined: no resource has been reallocated.')
                print('This request has been marked as resolved.')
                logging.debug("Request declined.")

    def deactivation_request_notification(self):
        """
        This method is used to notify the Admin if any new requests for deactivation have been made.
        If no new requests made, the method returns False.
        If one or more request has been made, the users dataframe is returned.
        The users dataframe is created from the users.csv file.
        """

        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        nb_of_requests = len(users[users["deactivation_requested"] == 1])
        if nb_of_requests == 0:
            logging.debug("No deactivation requests.")
            return False  # returns nothing if no new requests
        elif nb_of_requests == 1:
            print(f'\n* You have received {nb_of_requests} new deactivation request. *')
            return users
        else:
            print(f'\n* You have received {nb_of_requests} new deactivation request. *')
            return users

    def check_deactivation_requests(self):
        """
        This method tells the Admin if volunteers have requested to deactivate their
        account, and informs the Admin of the steps to take.
        This is done by reading the users.csv file and calling the deactivate_account_request() method
        """
        logging.debug("Checking for deactivation requests.")
        users = self.deactivation_request_notification()
        if users is False:
            print("\nYou have not received any deactivation requests.")
            print("Returning to previous menu\n")
            return

        print("\n--------------------------------------------")
        print("    RESPOND TO DEACTIVATION REQUESTS")
        nb_of_requests = len(users[users["deactivation_requested"] == 1])

        if nb_of_requests == 1:
            # extracts the username of the user who requested deactivation
            user_deactivating = users.loc[users['deactivation_requested'] == 1, 'username'].item()

            # calls method to deactivate the account
            logging.debug("Processing next request.")
            self.deactivate_account_request(df=users, user=user_deactivating)
            logging.debug("Finished processing deactivation requests.")

            # saves changes to the users.csv file
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print('The deactivation request has been processed!')
            return

        else:
            # extracts the usernames of users that requested deactivation into a list
            users_deactivating = users.loc[users['deactivation_requested'] == 1, 'username'].tolist()

            # calls the deactivation method for each username in the list
            for username in users_deactivating:
                logging.debug("Processing next request.")
                self.deactivate_account_request(df=users, user=username)
            logging.debug("Finished processing deactivation requests.")

            # saves the changes to the list
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print('All deactivation requests have been processed!')
            return

    def deactivate_account_request(self, df, user):
        """This method is called when an Admin wants to deactivate a volunteer's account following a request"""
        logging.debug(f"Admin prompted to confirm {user}'s deactivation request.")
        while True:
            print(f'\nUser {user} has requested to deactivate their account.\n')
            print('Enter [1] to deactivate {user}')
            print('Enter [2] to keep {user} active')
            print('Enter [0] to ignore this request for now.\n')
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break

        if option == 0:  # admin chose to ignore this request
            logging.debug("Request ignored.")
            return

        elif option == 1: # admin chose to deactivate account
            df.loc[df['username'] == user, ['deactivation_requested', 'active']] = 0
            print(f'\nYou have deactivated {user}')
            logging.info(f'Admin has deactivated {user}.')

            # decrement number of volunteers in camps file if user has a camp
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = users[users['username'] == user]
            cur_user = cur_user.replace({np.nan: None})
            camp_name = cur_user.iloc[0]['camp_name']
            if camp_name:
                plan_id = cur_user.iloc[0]['plan_id']
                camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
                user_camp = (camps['camp_name'] == camp_name)
                camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
                camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
                logging.debug("camps csv file updated")
                # delete the user's volunteering sessions
                vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
                vol_times = vol_times.drop(vol_times[vol_times['username'] == user].index)
                vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
                logging.debug("volunteering_times.csv updated")

        else: # admin chose to keep account active
            df.loc[df['username'] == user, 'deactivation_requested'] = 0
            print(f'\nYou have declined this request. {user} will remain active.')
            logging.info(f'Admin has declined deactivation request from {user}.')

    def end_event(self):
        """
        The method adds the end_date of the selected humanitarian plan.
        The selected plan is then closed and can no longer be updated.
        """
        plans = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        plans = plans[plans['end_date'].isna()]
        print("\n--------------------------------------------")
        print("\tEND HUMANITARIAN PLAN")
        if len(plans.index) == 0:
            print("There are no ongoing humanitarian plans.")
            logging.warning("No ongoing humanitarian plans. Returning to humanitarian plan menu.")
            return

        print("The following humanitarian plans are ongoing:")
        print("Number - Location - Start Date")
        for row in range(len(plans.index)):
            print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], sep=" - ")

        while True:
            logging.debug("Admin prompted to select humanitarian plan.")
            print("\nEnter [0] to return to the previous menu.")
            try:
                plan_num = int(input(">>Enter the number of the plan you would like to close: "))
                if plan_num == 0:
                    logging.debug("Returning to previous menu.")
                    return
                if plan_num not in range(1, len(plans.index) + 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a plan number corresponding to a humanitarian plan listed above.")
                logging.error("Invalid user input.")
                continue

            plans = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
            plans = plans.replace({np.nan: None})
            start = datetime.strptime(plans['start_date'].iloc[plan_num-1], "%d-%m-%Y").date()

            # enter end date
            while True:
                logging.debug("Admin prompted to enter end date.")
                print("\nEnter [0] to go back to the previous step.")
                end_date = input('>>Please input the end date of the event (DD-MM-YYYY): ')
                if end_date == "0":
                    logging.debug("Returning to previous step.")
                    break
                try:
                    end = datetime.strptime(end_date, "%d-%m-%Y").date()
                except ValueError:
                    print("\nIncorrect date format. Please use the format DD-MM-YYYY (e.g. 15-12-2023).")
                    logging.error("Invalid user input.")
                    continue
                t = datetime.now().date()
                if end > t:
                    print("\nEnd date cannot be in the future. Please try again.")
                    logging.error("Admin entered an end date in the future.")
                    continue
                if end < start:
                    print("\nEnd date cannot be earlier than start date. Please try again.")
                    logging.error("Admin entered an end date before the plan's start date.")
                    continue
                break
            if end_date == "0":  # return to plan selection
                continue
            break

        # update csv files: add end date; remove volunteer accounts and volunteering sessions for that plan
        plans.loc[plan_num - 1, 'end_date'] = end_date
        plan_id = plans['plan_id'].iloc[plan_num - 1]
        plans.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
        logging.debug("humanitarian_plan.csv updated")

        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        users = users.drop(users[users['plan_id'] == plan_id].index)
        users.to_csv(os.path.join('data', 'users.csv'), index=False)
        logging.debug("users.csv updated")

        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        vol_times = vol_times.drop(vol_times[vol_times['plan_id'] == plan_id].index)
        vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
        logging.debug("volunteering_times.csv updated")

        logging.debug(f"End date added to {plan_id}. The plan has been closed.")
        print("\nThe humanitarian plan", plan_id, "has been closed, with end date", end_date + ".")
        return

    def display_resources(self, hum_plan):
        """
        This method requires a HumanitarianPlan object as argument
        and prints out the corresponding resources .csv file.
        """
        resources = pd.read_csv(os.path.join('data', hum_plan))
        print(resources)

    def update_resources_in_storage(self):
        """
        This method allows the admin to request for additional resources to be added to storage for a selected humanitarian plan.
        A menu enables the admin to request for multiple resources before leaving the method.
        """
        print("\n--------------------------------------------")
        print("    REQUEST RESOURCES FOR STORAGE")
        plan_id = select_plan()  # user selects which plan they would like to update
        if plan_id == 0:
            logging.debug("Returning to resources menu.")
            return

        location = plan_id[:-5]
        plans_overview = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv')) #calls the humanitarian plan csv
        # plan_info = plans_overview.loc[plans_overview.location == location, ['location', 'food_storage', 'water_storage', 'firstaid_kits_storage']]

        print(f"\nCurrently, the resources in storage are as follows:"
              f"\n{plans_overview.loc[plans_overview.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
        logging.debug("Admin has been shown a summary of information contained in humanitarian plan csv.")

        while True:
            chosen_plan = plans_overview[plans_overview['plan_id'] == plan_id]
            current_food_storage = chosen_plan.iloc[0]['food_storage']
            current_water_storage = chosen_plan.iloc[0]['water_storage']
            current_aid_storage = chosen_plan.iloc[0]['firstaid_kits_storage']
            logging.debug("Admin prompted to select which resource they would like to restock.")
            while True:
                print("\nWhich resources would you like to request more of?")
                print("Enter [1] to request extra food")
                print("Enter [2] to request extra water")
                print("Enter [3] to request extra first-aid kits")
                print("Enter [0] to return to the previous menu\n")
                try:
                    resource_choice = int(input('>>Select an option: '))
                    if resource_choice not in range(4):
                        raise ValueError
                except ValueError:
                    logging.error('Invalid user input.')
                    print('\nPlease enter a number from the options provided.')
                    continue
                break

            if resource_choice == 0:
                logging.debug("Finished requesting resources for storage. Returning to resources menu.")
                return

            if resource_choice == 1:
                logging.debug("Admin has chosen to request more food resources.")
                print(f"\n{plan_id} currently has {current_food_storage} food packets in storage.")
                # asks user for how much more food they would like, checks this is a positive integer
                logging.debug(f"Admin prompted to enter number of additional food packets needed for {plan_id}.")
                while True:
                    print("\nEnter [B] to return to the previous step.")
                    amount_requested = input(f">>Enter the number of additional food packets "
                                             f"you would like to request for {plan_id}: ")
                    if amount_requested.upper() == "B":
                        logging.debug("Returning to previous step.")
                        break
                    try:
                        amount = int(amount_requested)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        logging.error("Invalid user input.")
                        print("\nPlease enter a positive integer.")
                        continue

                    # checks the total food in storage is a positive value, tells user that request for more food has been processed
                    total_food = current_food_storage + amount
                    #if total_food >10000:
                        #print(f"\n{plan_id} has a capacity of 10,000 for food storage. Your request will bring the total to {total_food}, please reduce your request.")
                        #logging.info(f"Admin has requested an amount of food packets that will exceed current storage capabilities. They have been asked to re-enter how many they would like.")
                        #resource_choice = 1
                        #continue
                    if total_food < 0:
                        print(f"\n{plan_id} still has insufficient food supplies. Please request more.")
                        continue
                    else:
                        logging.debug(
                            f"Admin has requested an additional {amount} food packets, bringing the total for {plan_id} to {total_food}.")
                        plans_overview.loc[plans_overview['location'] == location, 'food_storage'] = int(total_food)
                        plans_overview.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
                        logging.debug("humanitarian_plan.csv updated")
                        print(f"\nProcessing your request for an additional {amount} food packets ... \n"
                              f"\n{plan_id} now has a total of {total_food} food packets.")
                    break  # goes back to selection of resource from here

            if resource_choice == 2:
                logging.debug("Admin has chosen to request more water resources.")
                print(f"\n{plan_id} currently has {current_water_storage} water portions in storage.")

                # asks user for how much more water they would like, checks this is a positive integer
                logging.debug(f"Admin prompted to enter number of additional water portions needed for {plan_id}.")
                while True:
                    print("\nEnter [B] to return to the previous step.")
                    amount_requested = input(f'>>Enter the number of additional water portions you would like to request for {plan_id}: ')
                    if amount_requested.upper() == "B":
                        logging.debug("Returning to previous step.")
                        break
                    try:
                        amount = int(amount_requested)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        logging.error("Invalid user input.")
                        print("\nPlease enter a positive integer.")
                        continue

                    # checks the total water in storage is a positive value, tells user that request for more food has been processed
                    total_water = current_water_storage + amount
                    if total_water < 0:
                        print(f"\n{plan_id} still has insufficient water supplies. Please request more.")
                        continue
                    else:
                        logging.debug(
                            f"Admin has requested an additional {amount} water bottles, bringing the total for {plan_id} to {total_water}.")
                        plans_overview.loc[plans_overview['location'] == location, 'water_storage'] = int(total_water)
                        plans_overview.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
                        logging.debug("humanitarian_plan.csv updated")
                        print(f"\nProcessing your request for an additional {amount} water portions ... \n"
                              f"\n{plan_id} now has a total of {total_water} water portions.")
                    break

            if resource_choice == 3:
                logging.debug("Admin has chosen to request more first-aid kits.")
                print(f"\n{plan_id} currently has {current_aid_storage} first-aid kits in storage.")

                # asks user for how many more first aid kits they would like, checks this is a positive integer
                logging.debug(f"Admin prompted to enter number of additional first-aid kits needed for {plan_id}.")
                while True:
                    print("\nEnter [B] to return to the previous step.")
                    amount_requested = input(
                        f'>>Enter the number of additional first-aid kits you would like to request for {plan_id}: ')
                    if amount_requested.upper() == "B":
                        logging.debug("Returning to previous step.")
                        break
                    try:
                        amount = int(amount_requested)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        logging.error("Invalid user input.")
                        print("\nPlease enter a positive integer.")
                        continue

                    # checks the total first aid kits in storage is a positive value, tells user that request for more first aid kits has been processed
                    total_aid = current_aid_storage + amount
                    if total_aid < 0:
                        print(f"\n{plan_id} still has insufficient first-aid kits. Please request more.")
                        continue
                    else:
                        logging.debug(
                            f"Admin has requested an additional {amount} first aid kits, bringing the total for {plan_id} to {total_aid}.")
                        plans_overview.loc[plans_overview['location'] == location, 'firstaid_kits_storage'] = int(total_aid)
                        plans_overview.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
                        logging.debug("humanitarian_plan.csv updated")
                        print(f"\nProcessing your request for an additional {amount} first aid kits ... \n"
                              f"\n{plan_id} now has a total of {total_aid} first aid kits.")
                    break


    def allocate_resources(self, hum_plan, location):
        """
        This method requires a HumanitarianPlan object as argument, retrieves the
        corresponding resources .csv file and allows admin to allocate resources
        (Food packs, Water or First-Aid Kits) to camps in that HumanitarianPlan from storage.
        """
        resources = pd.read_csv(os.path.join('data', hum_plan))
        humani_plan = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        print(f"\nCurrently, the resources in storage are as follows:"
              f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
        print(f"And the resources in {hum_plan[:-4]} are as follows:"
              f"\n{resources.to_string(index=False)}")

        logging.debug("Admin prompted to select camp.")
        camp_format = False
        while camp_format == False:
            camp_no = v.integer("\nEnter [0] to return to the previous menu."
                                "\n>>Enter the number of the camp to which you would like to allocate resources: ")
            if camp_no == 0:
                logging.debug("Returning to previous menu.")
                return
            if any(resources['camp_name'].str.contains(f"Camp {camp_no}")):
                camp_format = True
            else:
                print('Please enter the number of an existing camp in this humanitarian plan.')
                logging.error("Invalid user input.")

        # loop allows multiple resources to be allocated without re-selecting camp
        logging.debug("Admin prompted to select which resource to allocate.")
        while True:
            print("\nChoose the resource you would like to allocate to Camp", camp_no, "of plan", hum_plan[:-4] + ".")
            print("Enter [1] for food packets")
            print("Enter [2] for water portions")
            print("Enter [3] for first-aid kits")
            print("Enter [0] to finish and return to the previous menu\n")
            try:
                resource_choice = int(input('>>Select an option: '))
                if resource_choice not in range(4):
                    raise ValueError
            except ValueError:
                print('\nPlease enter a number from the options provided.')
                logging.error("Invalid user input.")
                continue
            if resource_choice == 0:
                resources.to_csv(os.path.join('data', hum_plan), index=False)
                humani_plan.to_csv(os.path.join('data', 'humanitarian_plan.csv'), index=False)
                logging.debug("Finished allocating resources. humanitarian_plan.csv and camps csv file saved.")
                print(f"\nReturning to admin resources menu."
                      f"\nThe resources in {hum_plan[:-4]} are as follows:"
                      f"\n{resources}")
                print(f"\nAnd the remaining resources in storage: "
                      f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}")
                return
            if resource_choice == 1:
                logging.debug("Admin prompted to enter number of food packets to allocate.")
                while True:
                    print("\nEnter [B] to go back to the previous step.")
                    amount = input(f'>>Enter the number of food packets you would like to allocate to Camp {camp_no}: ')
                    if amount.upper() == "B":
                        logging.debug("Returning to previous step.")
                        break
                    try:
                        amount = int(amount)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a positive integer.")
                        logging.error("Invalid user input.")
                        continue
                    # making sure number of {resource} entered does not exceed number in storage
                    in_storage = humani_plan.loc[humani_plan['location'] == location, 'food_storage']
                    if any(in_storage - amount < 0):
                        print('\nThe amount entered exceeds the amount available in storage.'
                              '\nPlease check the amount in storage and try again.')
                        logging.warning("Insufficient resources in storage. Unable to allocate.")
                    else:
                        humani_plan.loc[humani_plan['location'] == location, 'food_storage'] -= int(amount)
                        resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'food'] += int(
                            amount)  # like a = a + food
                        print("\nAllocation complete.")
                        logging.debug(f"Allocated {amount} food packets.")
                        break
            if resource_choice == 2:
                logging.debug("Admin prompted to enter number of water portions to allocate.")
                while True:
                    print("\nEnter [B] to go back to the previous step.")
                    amount = input(f'>>Enter the number of water portions you would like to allocate to Camp {camp_no}: ')
                    if amount.upper() == "B":
                        logging.debug("Returning to previous step.")
                        break
                    try:
                        amount = int(amount)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a positive integer.")
                        logging.error("Invalid user input.")
                        continue
                    in_storage = humani_plan.loc[humani_plan['location'] == location, 'water_storage']
                    if any(in_storage - amount < 0):
                        print('\nThe amount entered exceeds the amount available in storage.'
                              '\nPlease check the amount in storage and try again.')
                        logging.warning("Insufficient resources in storage. Unable to allocate.")
                    else:
                        humani_plan.loc[humani_plan['location'] == location, 'water_storage'] -= int(amount)
                        resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'water'] += int(
                            amount)  # like a = a + food
                        print("\nAllocation complete.")
                        logging.debug(f"Allocated {amount} water portions.")
                        break
            if resource_choice == 3:
                logging.debug("Admin prompted to enter number of first-aid kits to allocate.")
                while True:
                    print("\nEnter [B] to go back to the previous step.")
                    amount = input(f'>>Enter the number of first-aid kits you would like to allocate to Camp {camp_no}: ')
                    if amount.upper() == "B":
                        logging.debug("Returning to previous step.")
                        break
                    try:
                        amount = int(amount)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a positive integer.")
                        logging.error("Invalid user input.")
                        continue
                    in_storage = humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage']
                    if any(in_storage - amount < 0):
                        print('\nThe amount entered exceeds the amount available in storage.'
                              '\nPlease check the amount in storage and try again.')
                        logging.warning("Insufficient resources in storage. Unable to allocate.")
                    else:
                        humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'] -= int(amount)
                        resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'firstaid_kits'] += int(
                            amount)  # like a = a + food
                        print("\nAllocation complete.")
                        logging.debug(f"Allocated {amount} first-aid kits.")
                        break

    def record_resource_consumption(self):
        """
        Enables the admin to record consumption of resources at a selected camp.
        A menu enables the admin to update multiple resources before leaving the method.
        """
        print("\n--------------------------------------------")
        print("\tRECORD RESOURCE CONSUMPTION")
        print("Select the camp at which resources have been consumed.")
        progress = 0
        while progress < 3:
            if progress == 0:
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to previous menu.")
                    return
                else:
                    progress += 1

            if progress == 1:
                camp_name = select_camp(plan_id)
                if camp_name == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif camp_name == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            if progress == 2:
                # outer loop to edit multiple attributes, exit if 0 is entered
                while True:
                    # inner loop to catch invalid input
                    logging.debug("Admin prompted to select which resource to update.")
                    while True:
                        print("\nWhich resource would you like to update?")
                        print("Enter [1] for consumption of food packets")
                        print("Enter [2] for consumption of water portions")
                        print("Enter [3] for use of first-aid kits")
                        print("Enter [9] to go back to camp selection")
                        print("Enter [0] to return to the previous menu\n")
                        try:
                            option = int(input(">>Select an option: "))
                            if option not in (0, 1, 2, 3, 9):
                                raise ValueError
                        except ValueError:
                            print("\nPlease enter a number from the options provided.")
                            logging.error("Invalid user input.")
                            continue
                        break

                    if option == 0:
                        logging.debug("Finished recording resource consumption. Returning to the resources menu.")
                        return
                    if option == 9:
                        logging.debug("Returning to previous step.")
                        progress -= 1
                        break
                    if option == 1:
                        resource_consumption.edit_food(plan_id, camp_name)
                    if option == 2:
                        resource_consumption.edit_water(plan_id, camp_name)
                    if option == 3:
                        resource_consumption.edit_medical_supplies(plan_id, camp_name)

    def admin_menu(self):
        """Main menu when the admin logs in, providing options to access sub-menus categorising the various admin functionalities."""
        while self.logged_in:
            logging.debug("Admin has entered the admin menu.")
            print("\n--------------------------------------------")
            print("\t\tADMIN MENU")
            print("Welcome, admin!")
            logging.debug("Checking for deactivation requests.")
            self.deactivation_request_notification()
            logging.debug("Checking for resource requests.")
            self.resource_request_notification()
            logging.debug("Checking if any camps are low on resources.")
            self.low_resources_notification()
            while True:
                print("\nChoose what you would like to do.")
                print("Enter [1] to create, display, edit or end a humanitarian plan")
                print("Enter [2] to manage volunteer accounts (including camp identification)")
                print("Enter [3] to manage resources at humanitarian plans")
                print("Enter [4] to manage refugee profiles")
                print("Enter [5] to manage volunteering sessions")
                print("Enter [0] to logout\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(6):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.info(f"Admin has logged out of their session.")
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
                logging.debug(f"Admin has selected the refugee profile menu.")
                self.refugee_menu()
            if option == 5:
                logging.debug(f"Admin has selected the volunteering session menu.")
                self.volunteering_session_menu()

    def hum_plan_menu(self):
        """Sub-menu enabling the admin to access functionalities relating to humanitarian plans."""
        while True:
            logging.debug("Admin has entered the humanitarian plan menu.")
            print("\n--------------------------------------------")
            print("\t\tHUMANITARIAN PLANS")
            while True:
                print("Enter [1] to create a humanitarian plan")
                print("Enter [2] to display a humanitarian plan")
                print("Enter [3] to edit a humanitarian plan (i.e. description, no. of camps)")
                print("Enter [4] to update a camp's capacity")
                print("Enter [5] to end a humanitarian plan")
                print("Enter [0] to return to the admin menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(6):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f"Admin has chosen to create a humanitarian plan.")
                self.create_hum_plan()
            if option == 2:
                logging.debug(f"Admin has chosen to display a humanitarian plan.")
                self.display_hum_plan()
            if option == 3:
                logging.debug(f"Admin has chosen to edit a humanitarian plan.")
                self.edit_hum_plan()
            if option == 4:
                logging.debug(f"Admin has chosen to update a camp's capacity.")
                self.update_camp_capacity()
            if option == 5:
                logging.debug(f"Admin has chosen to end a humanitarian plan.")
                self.end_event()

    def vol_accounts_menu(self):
        """Sub-menu enabling the admin to access functionalities relating to volunteer accounts."""
        while True:
            logging.debug("Admin has entered the volunteer accounts menu.")
            print("\n--------------------------------------------")
            print("\tMANAGE VOLUNTEER ACCOUNTS")
            while True:
                print("Enter [1] to create a volunteer account")
                print("Enter [2] to view a volunteer's details")
                print("Enter [3] to edit a volunteer's details")
                print("Enter [4] to update a volunteer's camp identification")
                print("Enter [5] to deactivate or reactivate a volunteer account")
                print("Enter [6] to respond to deactivation requests from volunteers")
                print("Enter [7] to delete a volunteer account")
                print("Enter [0] to return to the admin menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(8):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
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
                logging.debug(f"Admin has chosen to respond to deactivation requests from volunteers.")
                self.check_deactivation_requests()
            if option == 7:
                logging.debug(f"Admin has chosen to delete a volunteer account.")
                self.delete_volunteer()

    def resources_menu(self):
        """Sub-menu enabling the admin to access functionalities relating to resource allocation to camps."""
        while True:
            logging.debug("Admin has entered the resources menu.")
            print("\n--------------------------------------------")
            print("\t\tMANAGE RESOURCES")
            while True:
                print("Enter [1] to display resources for a humanitarian plan")
                print("Enter [2] to manually allocate resources to camps in a humanitarian plan")
                print("Enter [3] to use auto-allocating feature")
                print("Enter [4] to respond to resource requests from volunteers")
                print("Enter [5] to request additional resources be added to storage")
                print("Enter [6] to record consumption of resources at a camp")
                print("Enter [0] to return to the admin menu\n")
                try:
                    user_input = input(">>Select an option: ")
                    option = int(user_input)
                    logging.debug(f'Admin has entered {user_input}.')
                    if option not in range(7):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f"Admin has chosen to display resources.")
                print("\n--------------------------------------------")
                print("\t\tDISPLAY RESOURCES")
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to resources menu.")
                    continue
                plan_csv = plan_id + ".csv"
                logging.debug(f"Displaying resources for {plan_id}.")
                print(f"\nopening {plan_csv}...\n")
                self.display_resources(plan_csv)
            if option == 2:
                logging.debug(f"Admin has chosen to allocate resources manually.")
                print("\n--------------------------------------------")
                print("\tMANUALLY ALLOCATE RESOURCES")
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to resources menu.")
                    continue
                hum_plan = plan_id + ".csv"
                location = plan_id[:-5]
                logging.debug(f"Allocating resources manually to {plan_id}.")
                self.allocate_resources(hum_plan, location)
            if option == 3:  # auto-allocate
                logging.debug(f"Admin has chosen to auto-allocate resources.")
                print("\n--------------------------------------------")
                print("\tAUTO-ALLOCATE RESOURCES")
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to resources menu.")
                    continue
                hum_plan = plan_id + ".csv"
                location = plan_id[:-5]
                print(f"\nYou have selected {plan_id}.\n")

                logging.debug(f"Admin is prompted to select between allocating to all camps and allocating to a specific camp at {plan_id}.")
                print("\nWould you like to auto-allocate resources to all camps or select a camp?")
                print("Auto-allocating feature will top up resources to all camps for the following 7 days.")
                print("Enter [1] to allocate resources to all camps")
                print("Enter [2] to allocate resources to a specific camp")
                print("Enter [0] to return to the previous menu\n")
                while True:
                    option = v.integer(">>Select an option: ")
                    if option not in range(3):
                        print("\nPlease enter a number from the options provided.")
                        logging.error("Invalid user input.")
                        continue
                    break
                if option == 1:
                    logging.debug("Admin has chosen to auto-allocate to all camps.")
                    auto_resources.auto_all(hum_plan, location)
                if option == 2:
                    logging.debug("Admin has chosen to auto-allocate to a specific camp.")
                    auto_resources.auto_one(hum_plan, location)
                if option == 0:
                    logging.debug("Returning to the resources menu.")
            if option == 4:
                logging.debug(f"Admin has chosen to respond to resource requests.")
                self.resource_request_menu()
            if option == 5:
                logging.debug("Admin has chosen to request more resources for a humanitarian plan.")
                self.update_resources_in_storage()
            if option == 6:
                logging.debug("Admin has chosen to record consumption of resources at a camp.")
                self.record_resource_consumption()

    def refugee_menu(self):
        """Sub-menu enabling the admin to access functionalities relating to refugee profiles."""
        while True:
            logging.debug("Admin has entered the refugee profile menu.")
            print("\n--------------------------------------------")
            print("\tMANAGE REFUGEE PROFILES")
            while True:
                print("Enter [1] to create a new refugee profile")
                print("Enter [2] to view a refugee profile")
                print("Enter [3] to edit or remove a refugee profile")
                print("Enter [0] to return to the admin menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(4):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f"Admin has returned to the admin menu.")
                return
            if option == 1:
                logging.debug(f'Admin has chosen to create a refugee profile.')
                self.create_refugee_profile()
            if option == 2:
                logging.debug(f'Admin has chosen to view a refugee profile.')
                self.view_refugee_profile()
            if option == 3:
                logging.debug(f'Admin has chosen to edit or remove a refugee profile.')
                self.edit_refugee_profile()

    def volunteering_session_menu(self):
        """Sub-menu enabling the admin to access functionalities relating to volunteering sessions."""
        while True:
            logging.debug("Admin has entered the refugee profile menu.")
            print("\n--------------------------------------------")
            print("\tMANAGE VOLUNTEERING SESSIONS")
            users = pd.read_csv(os.path.join('data', 'users.csv'))
            users = users[(users['account_type'] == "volunteer") & (users['active'] == 1)]
            if len(users.index) == 0:
                print("There are no active volunteer accounts.")
                return

            while True:
                print("Enter [1] to add a volunteering session")
                print("Enter [2] to view a volunteer's volunteering sessions")
                print("Enter [3] to remove a volunteering session")
                print("Enter [0] to return to the admin menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(4):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f'Admin has returned to the volunteer menu.')
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
        """Changes the user's logged_in attribute to False, causing the user to log out."""
        self.logged_in = False
        print("You are now logged out. See you again!\n")

    def display_hum_plan(self):
        """
        Prompts the admin to select a humanitarian plan.
        Displays details of the selected plan.
        Details of the camps and resources in storage are only displayed if the selected plan is ongoing.
        """
        print("\n--------------------------------------------")
        print("\tDISPLAY HUMANITARIAN PLAN")
        plans = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
        if len(plans.index) == 0:
            print("No humanitarian plans have been created.")
            logging.warning("No humanitarian plans created.")
            return

        plans = plans.replace({np.nan: None})
        print("Number - Location - Start Date - End Date")
        for row in range(len(plans.index)):
            print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], plans['end_date'].iloc[row],
                  sep=" - ")

        logging.debug("Admin prompted to select humanitarian plan.")
        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                plan_num = int(input(">>Enter the number of the plan you would like to display: "))
                if plan_num == 0:
                    logging.debug("Returning to previous menu.")
                    return
                if plan_num not in range(1, len(plans.index) + 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a plan number corresponding to a humanitarian plan listed above.")
                logging.error("Invalid user input.")
                continue
            break

        plan_id = plans.loc[plan_num - 1, 'plan_id']
        end_date = plans.loc[plan_num - 1, 'end_date']
        logging.debug(f"Displaying details of {plan_id}.")
        print("\nDetails of humanitarian plan:")
        print("Location:", plans.loc[plan_num - 1, 'location'])
        print("Description:", plans.loc[plan_num - 1, 'description'])
        print("Number of camps:", plans.loc[plan_num - 1, 'number_of_camps'])
        print("Start date:", plans.loc[plan_num - 1, 'start_date'])
        print("End date:", end_date)
        # only print resources and camp details if plan is ongoing
        if not end_date:
            print("Food packets in storage:", plans.loc[plan_num - 1, 'food_storage'])
            print("Water portions in storage:", plans.loc[plan_num - 1, 'water_storage'])
            print("First-aid kits in storage:", plans.loc[plan_num - 1, 'firstaid_kits_storage'])

            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            print("\nCamps in humanitarian plan:")
            print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
            for row in range(len(camps.index)):
                print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                      str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
                      sep=" - ")
        else:
            print("This plan has been closed.")
        return

    def update_camp_capacity(self):
        """
        Enables the admin to update the refugee capacity of a selected camp within a humanitarian plan.
        """
        print("\n--------------------------------------------")
        print("\tUPDATE CAMP CAPACITY")
        print("Select the camp whose capacity you would like to update.")
        progress = 0
        while progress < 3:
            if progress == 0:
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to previous menu.")
                    return
                else:
                    progress += 1

            if progress == 1:
                camp_name = select_camp(plan_id)
                if camp_name == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif camp_name == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            if progress == 2:
                camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
                cur_camp = camps[camps['camp_name'] == camp_name]
                print("\nCurrent capacity of " + camp_name + ": " + str(cur_camp.iloc[0]['capacity']))
                print("The camp currently has " + str(cur_camp.iloc[0]['refugees']) + " refugees.")
                logging.debug(f"Admin prompted to enter new capacity of {plan_id}, {camp_name}.")
                while True:
                    print("\nEnter [X] to return to the previous menu or [B] to go back to camp selection.")
                    new_capacity = input(">>New capacity: ")
                    if new_capacity.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    if new_capacity.upper() == "B":
                        logging.debug("Returning to previous step.")
                        progress -= 1
                        break
                    try:
                        new_capacity = int(new_capacity)
                        if new_capacity < 1:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a positive integer.")
                        logging.error("Invalid user input.")
                        continue
                    if new_capacity < cur_camp.iloc[0]['refugees']:
                        print("\nInvalid input: New capacity is less than refugee population. "
                              "\nPlease try again or return to the previous menu.")
                        logging.error("Capacity entered is less than the current refugee population.")
                        continue
                    if new_capacity == cur_camp.iloc[0]['capacity']:
                        print("\nCapacity is unchanged. Please try again or return to the previous step.")
                        logging.error("Capacity is unchanged.")
                        continue
                    progress += 1
                    break

        logging.debug("Capacity updated successfully.")
        # update csv file
        chosen = (camps['camp_name'] == camp_name)
        camps.loc[chosen, 'capacity'] = new_capacity
        camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
        logging.debug("camps csv file updated")
        print("Capacity updated successfully!")
        print("You have updated the capacity of", plan_id + ",", camp_name, "to", str(new_capacity) + ".")

    def view_volunteer(self):
        """Enables the admin to view the personal details and camp identification of a selected volunteer."""
        print("\n--------------------------------------------")
        print("\tVIEW VOLUNTEER DETAILS")
        print("Select the volunteer whose details you are viewing.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            username = selected[2]

        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        select_user = users[users['username'] == username]
        select_user = select_user.replace({np.nan: None})
        gender_str = convert_gender(select_user.iloc[0]['gender'])

        logging.debug(f"Displaying personal information of {username}.")
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
        return

    def update_volunteer_camp(self):
        """
        Enables the admin to update the camp identification of a selected active volunteer.
        If the volunteer currently does not have a camp, the admin is prompted to select a camp.
        If the volunteer currently has a camp, the admin can select whether to change the camp or remove the volunteer's camp identification.
        """
        print("\n--------------------------------------------")
        print("  UPDATE VOLUNTEER'S CAMP IDENTIFICATION")
        print("Select the volunteer whose camp identification you are updating.")
        selected = select_plan_camp_vol(active=1, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            plan_id, camp_name, username = selected

        def add_camp(plan_id):
            """Prompts the admin to select a camp for the chosen volunteer if they currently do not have a camp."""
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            print(username, "currently has no camp identification.")
            logging.debug(f"Admin prompted to add a camp for {username}.")
            while True:
                print("\nEnter [X] to return to the previous menu.")
                print("Choose a camp.")
                print("\nCamp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                camp_num = input("\n>>Enter the number of the camp the volunteer will join (e.g. [1] for Camp 1): ")
                if camp_num.upper() == "X":
                    logging.debug("Returning to previous menu without making changes.")
                    return None
                try:
                    camp_num = int(camp_num)
                    if camp_num not in range(1, len(camps.index) + 1):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter the number of a camp from the list displayed.")
                    logging.error("Invalid user input.")
                    continue
                new_camp = "Camp " + str(camp_num)
                logging.debug(f"{username} has been assigned to {new_camp} at {plan_id}.")
                return new_camp

        def edit_camp(plan_id, camp_name):
            """Prompts the admin to select a new camp for the chosen volunteer if they currently have a camp."""
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            print(username + "'s current camp is:", camp_name)
            if len(camps.index) == 1:
                print("There is currently only one camp. It is not possible to change camp identification.")
                logging.warning(f"There is only one camp at {plan_id}. Not possible to change camps.")
                return camp_name

            logging.debug("Admin prompted to select new camp.")
            while True:
                print("\nEnter [X] to return to the previous menu.")
                print("Choose a new camp.")
                print("Camp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                camp_num = input(">>Enter the number of the camp the volunteer will join (e.g. [1] for Camp 1): ")
                if camp_num.upper() == "X":
                    logging.debug("Returning to previous menu without making changes.")
                    return camp_name
                try:
                    camp_num = int(camp_num)
                    if camp_num not in range(1, len(camps.index) + 1):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter the number of a camp from the list displayed.")
                    logging.error("Invalid user input.")
                    continue
                new_camp = "Camp " + str(camp_num)
                if new_camp == camp_name:
                    print("\nNew camp is the same as current camp. Please try again or return to the previous menu.")
                    logging.error("Camp is unchanged.")
                    continue
                logging.debug(f"{username} has been assigned to {new_camp} at {plan_id}.")
                return new_camp

        if not camp_name:
            new_camp = add_camp(plan_id)
        else:
            logging.debug(f"Admin prompted to choose between updating and removing {username}'s camp identification.")
            while True:
                print("\nEnter [1] to update camp identification")
                print("Enter [2] to remove camp identification")
                print("Enter [0] to return to the previous menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(3):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue

                if option == 0:
                    logging.debug("Returning to previous menu.")
                    return
                if option == 1:
                    new_camp = edit_camp(plan_id, camp_name)
                if option == 2:
                    logging.debug("Admin prompted to confirm removal of camp identification.")
                    while True:
                        print("\nAre you sure you would like to remove the camp identification of", username + "?")
                        print("All volunteering sessions for this volunteer will be erased.")
                        print("Enter [1] to proceed")
                        print("Enter [0] to go back to the previous step\n")
                        try:
                            remove_option = int(input(">>Select an option: "))
                            if remove_option not in (0, 1):
                                raise ValueError
                        except ValueError:
                            print("\nPlease enter a number from the options provided.")
                            logging.error("Invalid user input.")
                            continue
                        break
                    if remove_option == 0:
                        logging.debug("Returning to previous step.")
                        continue
                    logging.debug(f"Removed {username}'s camp identification.")
                    new_camp = None
                break

        # update csv files
        if new_camp != camp_name:
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == username)
            users.loc[cur_user, 'camp_name'] = new_camp
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")

            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            if new_camp:
                chosen = (camps['camp_name'] == new_camp)
                camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            if camp_name:
                old = (camps['camp_name'] == camp_name)
                camps.loc[old, 'volunteers'] = camps.loc[old, 'volunteers'] - 1
            camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
            logging.debug("camps csv file updated")

            if camp_name and not new_camp:  # remove volunteering sessions
                vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
                vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
                vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
            if camp_name and new_camp:  # change camp_name in volunteering_times.csv
                vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
                vol_times.loc[vol_times["username"] == username, "camp_name"] = new_camp
                vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
            logging.debug("volunteering_times.csv updated")

            print("\n" + username + "'s new camp is:", new_camp)
        return

    def create_refugee_profile(self):
        """
        Enables the admin to create a refugee profile at a selected humanitarian plan and camp.
        The admin is prompted for the refugee's details one by one.
        """
        print("\n--------------------------------------------")
        print("\tADD REFUGEE PROFILE")

        progress = -2
        # loop allowing user to go back
        while progress < 6:
            if progress == -2:
                plan_id = select_plan()
                if plan_id == 0:
                    logging.debug("Returning to previous menu.")
                    return
                else:
                    progress += 1

            if progress == -1:
                camp_name = select_camp(plan_id)
                if camp_name == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif camp_name == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

                camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
                cur_camp = camps[camps['camp_name'] == camp_name]
                remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']

                if remaining_cap == 0:
                    print("\nThe selected camp has reached its maximum capacity. Unable to add new refugees.")
                    logging.warning("The selected camp is full. Returning to previous menu.")
                    return
                print("\nRemaining capacity of the selected camp is " + str(remaining_cap) + ".")
                print("Please return to the previous menu if the refugee's family is larger than this number.")

            if progress == 0:
                refugee_name = refugee_profile_funcs.add_name()
                if refugee_name == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif refugee_name == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 1:
                gender = refugee_profile_funcs.add_gender()
                if gender == 0:
                    logging.debug("Returning to previous menu.")
                    return
                elif gender == 9:
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                date_of_birth = refugee_profile_funcs.add_dob()
                if date_of_birth == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif date_of_birth == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                medical_cond = refugee_profile_funcs.add_medical_cond()
                if medical_cond == 0:
                    logging.debug("Returning to previous menu.")
                    return
                elif medical_cond == 9:
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 4:
                family = refugee_profile_funcs.add_family(remaining_cap)
                if family == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif family == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 5:
                remarks = refugee_profile_funcs.add_remarks()
                if remarks == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif remarks == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

        logging.debug("Admin has finished entering refugee details.")
        # Update csv tables
        refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
        if len(refugees.index) == 0:
            refugee_id = 1
        else:
            refugee_id = refugees['refugee_id'].iloc[-1] + 1
        new_row = {'refugee_id': [refugee_id], 'refugee_name': [refugee_name], 'gender': [gender],
                   'date_of_birth': [date_of_birth], 'plan_id': [plan_id], 'camp_name': [camp_name],
                   'medical_condition': [medical_cond], 'family_members': [family], 'remarks': [remarks]}
        new = pd.DataFrame(new_row)
        refugees = pd.concat([refugees, new], ignore_index=True)
        refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
        logging.debug("refugees.csv updated")

        camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
        chosen = (camps['camp_name'] == camp_name)
        camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] + family
        camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
        logging.debug("camps csv file updated")

        # Print details provided
        gender_str = convert_gender(gender)
        medical_str = convert_medical_condition(medical_cond)

        print("\nRefugee profile created!")
        print("Refugee ID: ", refugee_id)
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
        """Enables the admin to view the profile of a selected refugee."""
        print("\n--------------------------------------------")
        print("\tVIEW REFUGEE PROFILE")
        print("Select the refugee whose profile you are viewing.")
        selected = select_plan_camp_refugee()  # returns (plan_id, camp_name, refugee_id)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            plan_id, camp_name, refugee_id = selected

        refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
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

        logging.debug("Printing details of selected refugee.")
        print("\nDetails of refugee ID:", refugee_id)
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
        """
        Enables the admin to edit the profile of a selected refugee.
        Once a refugee is selected, a menu enables the admin to edit multiple details before leaving the method.
        This includes an option to remove the refugee's profile.
        """
        print("\n--------------------------------------------")
        print("    EDIT OR REMOVE REFUGEE PROFILE")
        print("Select the refugee whose profile you would like to edit.")
        selected = select_plan_camp_refugee()  # returns (plan_id, camp_name, refugee_id)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            plan_id, camp_name, refugee_id = selected

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
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
                logging.debug("Admin prompted to select which detail to edit.")
                print("\nWhich details would you like to update?")
                print("Enter [1] for refugee name")
                print("Enter [2] for gender")
                print("Enter [3] for date of birth")
                print("Enter [4] for medical condition")
                print("Enter [5] for no. of family members")
                print("Enter [6] for remarks")
                print("Enter [9] to remove the refugee's profile")
                print("Enter [0] to return to the previous menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in (0, 1, 2, 3, 4, 5, 6, 9):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break

            if option == 0:
                logging.debug("Finished editing refugee profile. Returning to refugee profile menu.")
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
        """
        Enables the admin to add a volunteering session for a selected volunteer.
        The admin is prompted for the date, start time and end time of the session.
        """
        print("\n--------------------------------------------")
        print("\tADD VOLUNTEERING SESSION")
        print("Select the volunteer for whom you are adding a session.")
        selected = select_plan_camp_vol(active=1, none=0)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            plan_id, camp_name, username = selected

        print("\nAdding a volunteering session for", username + "...")
        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        cur_user_times = vol_times[vol_times['username'] == username]
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])

        progress = 0
        # loop allowing user to go back
        while progress < 4:
            if progress == 0:
                vol_date = volunteering_session_funcs.select_date()
                if vol_date == "0":
                    logging.debug("Returning to previous menu.")
                    return
                else:
                    progress += 1

            elif progress == 1:
                start_time = volunteering_session_funcs.select_start_time(vol_date, cur_user_times)
                if start_time == "0":
                    logging.debug("Returning to previous menu.")
                    return
                elif start_time == "9":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                end_time = volunteering_session_funcs.select_end_time(start_time, cur_user_times)
                if end_time == "X":
                    logging.debug("Returning to previous menu.")
                    return
                elif end_time == "B":
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                confirm = volunteering_session_funcs.confirm_slot(start_time, end_time)
                if confirm == 0:
                    logging.debug("Returning to previous menu.")
                    return
                elif confirm == 9:
                    logging.debug("Returning to previous step.")
                    progress -= 1
                else:
                    progress += 1

        logging.debug(f"Admin has finished entering details of new volunteering session for {username}.")
        # update csv file
        vol_times = open(os.path.join('data', 'volunteering_times.csv'), "a")
        vol_times.write(f'\n{username},{plan_id},{camp_name},{start_time},{end_time}')
        vol_times.close()
        logging.debug("volunteering_times.csv updated")
        print("\nVolunteering session added successfully!")
        return

    def view_volunteering_sessions(self):
        """Enables the admin to view all volunteering sessions scheduled for a selected volunteer."""
        print("\n--------------------------------------------")
        print("\tVIEW VOLUNTEERING SESSIONS")
        print("Select the volunteer whose sessions you are viewing.")
        selected = select_plan_camp_vol(active=1, none=0)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            username = selected[2]

        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        cur_user_times = vol_times[vol_times['username'] == username]
        if len(cur_user_times.index) == 0:
            print(username, "does not have any volunteering sessions.")
            logging.info("No volunteering sessions for the selected volunteer.")
            return

        logging.debug(f"Displaying volunteering sessions for {username}.")
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])
        print(username, "has added the following volunteering sessions:")
        for row in range(len(cur_user_times.index)):
            print(str(row + 1) + ".", "Start:",
                  datetime.strptime(cur_user_times['start_time'].iloc[row], "%Y-%m-%d %H:%M").strftime(
                      "%d-%m-%Y %H:%M"),
                  "\t", "End:",
                  datetime.strptime(cur_user_times['end_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"))
        return

    def remove_volunteering_session(self):
        """Enables the admin to remove a volunteering session scheduled for a selected volunteer."""
        print("\n--------------------------------------------")
        print("\tREMOVE VOLUNTEERING SESSION")
        print("Select the volunteer for whom you are removing a session.")
        selected = select_plan_camp_vol(active=1, none=0)
        if selected == 0:
            logging.debug("Returning to previous menu.")
            return
        else:
            username = selected[2]

        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        cur_user_times = vol_times[vol_times['username'] == username]
        if len(cur_user_times.index) == 0:
            print(username, "does not have any volunteering sessions.")
            logging.warning("No volunteering sessions for the selected volunteer.")
            return
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])

        logging.debug(f"Admin prompted to select a volunteering session to remove for {username}.")
        while True:
            print("\nEnter [X] to return to the previous menu.")
            print(username + "'s volunteering sessions:")
            for row in range(len(cur_user_times.index)):
                start = datetime.strptime(cur_user_times['start_time'].iloc[row], '%Y-%m-%d %H:%M').strftime(
                    '%d-%m-%Y %H:%M')
                end = datetime.strptime(cur_user_times['end_time'].iloc[row], '%Y-%m-%d %H:%M').strftime(
                    '%d-%m-%Y %H:%M')
                print("[" + str(row + 1) + "]", "Start:", start, "\t", "End:", end)
            remove = input(">>Enter the number of the session you would like to remove: ").strip()
            if remove.upper() == "X":
                logging.debug("Returning to previous menu.")
                return
            try:
                remove = int(remove)
                if remove not in range(1, len(cur_user_times.index) + 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number corresponding to one of the above volunteering sessions.")
                logging.error("Invalid user input.")
                continue

            # confirmation
            start = datetime.strptime(cur_user_times['start_time'].iloc[remove - 1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            end = datetime.strptime(cur_user_times['end_time'].iloc[remove - 1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            while True:
                logging.debug(f"Admin prompted to confirm removal of volunteering session.")
                print("\nAre you sure you would like to remove the following session?")
                print("Start:", start, "\t", "End:", end)
                print("Enter [1] to proceed")
                print("Enter [0] to go back to the previous step\n")
                try:
                    remove_option = int(input(">>Select an option: "))
                    if remove_option not in (0, 1):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break
            if remove_option == 0:
                logging.debug("Returning to previous step.")
                continue
            logging.debug("Removal of volunteering session confirmed.")

            # update csv file
            vol_times = vol_times.drop(vol_times[(vol_times['username'] == username) &
                                                 (vol_times['start_time'] == cur_user_times['start_time'].iloc[
                                                     remove - 1])].index)
            vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
            logging.debug("volunteering_times.csv updated")
            print("\nVolunteering session has been removed.")
            return
