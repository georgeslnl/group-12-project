import pandas as pd, numpy as np
from datetime import datetime

import auto_resources
from humanitarianplan import HumanitarianPlan
from coded_vars import convert_gender, convert_medical_condition
from selection import select_plan, select_camp
from selection_volunteer import select_plan_camp_vol
from selection_refugees import select_plan_camp_refugee
import hum_plan_funcs, volunteer_funcs, refugee_profile_funcs, volunteering_session_funcs
import verify as v
import logging


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
           The method then creates a new HumanitarianPlan object but need not return it.
           It also adds the Humanitarian Plan to the csv file 'humanitarian_plan.csv'
           """
        print("\nCreate humanitarian plan")
        progress = 0
        while progress < 4:
            if progress == 0:
                desc = hum_plan_funcs.add_description()
                if desc == "0":
                    return
                else:
                    progress += 1

            if progress == 1:
                loc = hum_plan_funcs.add_location()
                if loc == "0":
                    return
                elif loc == "9":
                    progress -= 1
                else:
                    progress += 1

            if progress == 2:
                start_date = hum_plan_funcs.add_start_date(loc)
                if start_date == "0":
                    return
                elif start_date == "9":
                    progress -= 1
                else:
                    progress += 1

            if progress == 3:
                nb_of_camps = hum_plan_funcs.add_num_camps()
                if nb_of_camps == "X":
                    return
                elif nb_of_camps == "B":
                    progress -= 1
                else:
                    progress += 1

        # Creating humanitarian plan object
        hu_pl = HumanitarianPlan(desc, loc, start_date, nb_of_camps)
        name = f'{loc}_{start_date[6:]}'

        # Opens the csv file and adds the data for this humanitarian plan
        h = open("humanitarian_plan.csv", "a")
        h.write(f'\n{name},{desc},{loc},{start_date},{nb_of_camps},,{1000},{1000},{250}')  # default amount of resources
        # desc is wrapped in "" because we don't want to csv file to see a "," in the description as a delimitter
        h.close()

        # sort by plan_id after a new plan is added
        plans = pd.read_csv('humanitarian_plan.csv')
        plans = plans.sort_values(by=['plan_id'])
        plans.to_csv('humanitarian_plan.csv', index=False)

        # Prints out the information about the Humanitarian Plan created
        print(f'A new humanitarian plan has been created with the following information:'
              f'\n\t Description: {desc}'
              f'\n\t Location affected: {loc}'
              f'\n\t Start date of the event: {start_date}'
              f'\n\t Number of camps: {nb_of_camps}')
        return

    def edit_hum_plan(self):
        hum_plan_df = pd.read_csv('humanitarian_plan.csv')
        progress = 0
        print(f"Currently, the details of humanitarian plans are as follows:"
              f"\n {hum_plan_df}")
        while progress < 3:
            # if progress < 0:
            #     print('You have decided to return to the previous menu.')
            #     return
            if progress == 0:
                while True:
                    plan_index = v.integer('Please select the index of the humanitarian plan you wish to edit.'
                                           '(please note only the description or number of camps of the plan can be changed)')
                    plan_id = str(hum_plan_df.loc[hum_plan_df.index == plan_index,'plan_id'])
                    plan_id = plan_id.split('\n')[0]
                    plan_id = plan_id[5:]
                    if plan_index in range(0,len(hum_plan_df.plan_id)):
                        while True:
                            edit_choice = v.integer('Please choose what you would like to edit:'
                                                f'\nEnter [1] to change the description of {plan_id}.'
                                                f'\nEnter [2] to change the number of camps of {plan_id}.'
                                                f'\nEnter [0] to return to the previous menu. ')
                            if edit_choice in range(0,3):
                                break
                            else:
                                print('Number entered not in range [0-2].')
                        if edit_choice == 0:
                            return
                        elif edit_choice == 1 or edit_choice == 2:
                            progress += 1
                        break
                    else:
                        print('The index you entered is outside the range of humanitarian plans.')
            elif progress == 1:
                if edit_choice == 1:
                    cur_desc = str(hum_plan_df.loc[hum_plan_df.index == plan_index,"description"])
                    cur_desc = cur_desc.split('\n')[0]
                    cur_desc = cur_desc[5:]
                    print(f'You have chosen to edit the description of {plan_id}.'
                          f'\n The current description is:'
                          f'\n {cur_desc}')
                    while True:
                        edit_desc = v.integer("Enter [1] to edit the description."
                                              "\nEnter [0] to return to the previous step: ")
                        if edit_desc in range(0,2):
                            if edit_desc == 0:
                                progress -= 1
                                break
                            elif edit_desc == 1:
                                desc = hum_plan_funcs.edit_description(plan_id,plan_index,hum_plan_df)
                                if any(desc) == 'X':
                                    progress -= 1
                                else:
                                    progress += 1
                                break
                        else:
                            print('Number entered not in range [0-1].')
                elif edit_choice == 2:
                    num_camps = hum_plan_df.loc[hum_plan_df.index == plan_index, "number_of_camps"]
                    num_camps = num_camps[5:]
                    print(f'You have chosen to edit the number of camps of {plan_id}.'
                          f'\n The current number of camps is:'
                          f'\n {num_camps}')
                    progress += 1
            elif progress == 2:
                while True:
                    next = v.integer("Enter [1] to edit other details of humanitarian plans."
                                     "\nEnter [0] to exit the edit humanitarian plan function and return to the previous menu: ")
                    if next in range(0,2):
                        if next == 0:
                            return
                        elif next == 1:
                            progress = 0
                        break
                    else:
                        print('Number entered not in range [0-1].')



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

    # def edit_volunteer(self):
    #     df = pd.read_csv('users.csv')
    #     # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
    #     print(df.iloc[1:, 0])
    #     while True:
    #         user = v.string('Please enter the username of the volunteer whose account details you would like to modify.')
    #         if any(df['username'].str.contains(user)) == True: #testing if volunteer account already exists
    #             break
    #         else:
    #             print('Username entered does not match with any volunteer.')
    #             continue
    #     while True:
    #         # a list for admin to choose from, edited to work for the merged 'users' file
    #         print("Please choose one of the following details you would like to modify."
    #               "\n 0 for username"
    #               "\n 1 for password"
    #               "\n 2 for active status"
    #               "\n 3 for first name"
    #               "\n 4 for last name"
    #               "\n 5 for email address"
    #               "\n 6 for phone number"
    #               "\n 7 for gender"
    #               "\n 8 for date of birth"
    #               "\n 9 for plan ID"
    #               "\n 10 for camp name")
    #         index = int(v.integer(""))
    #         if index not in range(0, 11):
    #             print('Please enter an integer from 0-10.')
    #             continue
    #         else:
    #             #This is code to fix the index problem due to using the new 'users' file
    #             if index==2:
    #                 index=3
    #             elif index==0 or index==1:
    #                 pass
    #             else:
    #                 index+=2
    #             break
    #     temp_list = ['username', 'password', 'account_type', 'active_status', 'deactivation_requested',
    #                  'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'plan_id', 'camp_name']
    #     new = input("Please enter a new value: ")  # will be used to input into csv as status
    #     # and then enter a new value
    #     # create a dataform without that specific row where username is...
    #     df.loc[df['username'] == user, temp_list[index]] = new  # modify the dataform
    #     df.to_csv('users.csv', index=False)  # write it into the .csv file
    #     updated = df['username'] == user
    #     print("The updated account details of " + user + "is:\n", df[updated])

    # def create_volunteer(self):
    #     new = open("users.csv", "a")
    #
    #     username = v.string("Please enter an user name: ")
    #     pw = input("Please enter the password: ") #password should be just '111'
    #     first_name = v.name("Please enter the first name: ")
    #     last_name = v.name("Please enter the last name: ")
    #     email = v.email("PLease enter the email address: ")
    #     phone = v.integer("Please enter the phone number: ")
    #     gender = v.integer("Please enter the gender: ")
    #     DOB = v.date("Please enter the date of birth (DD-MM-YYYY): ")
    #     plan_id = v.string("Please enter the plan ID: ")
    #     camp_name = v.string("Please enter the camp name: ")
    #
    #     new.write(f'\n{username},{pw},volunteer,1,0,{first_name},{last_name},{email},{phone},{gender},{DOB},{plan_id},{camp_name}')
    #     new.close()
    #     print("New user added successfully.")
    #
    #     users = pd.read_csv('users.csv')
    #     new_account = users['username'] == username
    #     print("The new account details of", username, "is:\n", users[new_account])

    def create_volunteer(self):
        print("\nCreate volunteer account")
        print("You will be prompted to enter the volunteer's details.")

        progress = 0
        # loop allowing user to go back
        while progress < 10:
            if progress == 0:
                plan_id = volunteer_funcs.add_plan()
                if plan_id == "B":
                    return
                else:
                    progress += 1

            elif progress == 1:
                camp_name = volunteer_funcs.add_camp(plan_id)
                if camp_name == "X":
                    return
                elif camp_name == "B":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                username = volunteer_funcs.add_username()
                if username == "0":
                    return
                elif username == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                password = volunteer_funcs.add_password()
                if password == "0":
                    return
                elif password == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 4:
                first_name = volunteer_funcs.add_first_name()
                if first_name == "0":
                    return
                elif first_name == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 5:
                last_name = volunteer_funcs.add_last_name()
                if last_name == "0":
                    return
                elif last_name == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 6:
                gender = volunteer_funcs.add_gender()
                if gender == 0:
                    return
                elif gender == 9:
                    progress -= 1
                else:
                    progress += 1

            elif progress == 7:
                date_of_birth = volunteer_funcs.add_dob()
                if date_of_birth == "0":
                    return
                elif date_of_birth == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 8:
                email = volunteer_funcs.add_email()
                if email == "0":
                    return
                elif email == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 9:
                phone_number = volunteer_funcs.add_phone_num()
                if phone_number == "0":
                    return
                elif phone_number == "9":
                    progress -= 1
                else:
                    progress += 1

        # Update csv tables
        # users = open("users.csv", "a")
        # if camp_name:
        #     users.write(
        #         f'\n{username},{password},volunteer,1,0,{first_name},{last_name},{email},{phone_number},{gender},{date_of_birth},{plan_id},{camp_name}')
        # else:
        #     users.write(
        #         f'\n{username},{password},volunteer,1,0,{first_name},{last_name},{email},{phone_number},{gender},{date_of_birth},{plan_id},')
        # users.close()

        users = pd.read_csv('users.csv', dtype={'password': str})
        new_row = {'username': [username], 'password': [password], 'account_type': ['volunteer'], 'active': [1],
                   'deactivation_requested': [0], 'first_name': [first_name], 'last_name': [last_name],
                   'email': [email], 'phone_number': [phone_number], 'gender': [gender],
                   'date_of_birth': [date_of_birth], 'plan_id': [plan_id], 'camp_name': [camp_name]}
        new = pd.DataFrame(new_row)
        users = pd.concat([users, new], ignore_index=True)
        users = users.sort_values(by=['username'])  # sort by username before saving
        users.to_csv('users.csv', index=False)

        if camp_name:
            camps = pd.read_csv(plan_id + '.csv')
            chosen = (camps['camp_name'] == camp_name)
            camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            camps.to_csv(plan_id + '.csv', index=False)

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
        print("\nEdit volunteer details")
        print("Select the volunteer whose details you are updating.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            username = selected[2]

        users = pd.read_csv('users.csv', dtype={'password': str})
        select_user = users[users['username'] == username]
        password = select_user.iloc[0]['password']
        first_name = select_user.iloc[0]['first_name']
        last_name = select_user.iloc[0]['last_name']
        gender = select_user.iloc[0]['gender']
        date_of_birth = select_user.iloc[0]['date_of_birth']
        email = select_user.iloc[0]['email']
        phone_number = select_user.iloc[0]['phone_number']

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            # inner loop to catch invalid input
            while True:
                print("\nEdit details of", username)
                print("Enter [1] for username")
                print("Enter [2] for password")
                print("Enter [3] for first name")
                print("Enter [4] for last name")
                print("Enter [5] for gender")
                print("Enter [6] for date of birth")
                print("Enter [7] for email")
                print("Enter [8] for phone number")
                print("Enter [0] to return to the previous menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break

            if option == 0:
                return
            if option == 1:
                volunteer_funcs.edit_username(username)
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
        print("\nDelete volunteer account")
        print("Select the volunteer whose account you would like to delete.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            plan_id, camp_name, username = selected

        while True:
            print("\nAre you sure you would like to delete the account of", username + "?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the previous menu")
            try:
                user_input = input("Select an option: ")
                option = int(user_input)
                if option not in (0, 1):
                    logging.error(
                        f"Admin has entered {user_input} when trying to delete {username}'s account. ValueError raised.")
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 0:
            return

        # update csv files
        users = pd.read_csv('users.csv', dtype={'password': str})
        users = users.drop(users[users['username'] == username].index)
        users.to_csv('users.csv', index=False)

        vol_times = pd.read_csv("volunteering_times.csv")
        vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
        vol_times.to_csv('volunteering_times.csv', index=False)

        if camp_name:
            camps = pd.read_csv(plan_id + '.csv')
            user_camp = (camps['camp_name'] == camp_name)
            camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
            camps.to_csv(plan_id + '.csv', index=False)

        logging.info(f'{username} has been deleted by admin.')
        print(username + "'s account has been deleted successfully.")

    def active_volunteer(self):
        print("\nDeactivate or reactivate volunteer account")
        print("Select the volunteer whose account you would like to deactivate or reactivate.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            plan_id, camp_name, username = selected

        users = pd.read_csv('users.csv', dtype={'password': str})
        select_user = users[users['username'] == username]
        active = select_user.iloc[0]['active']

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
            print("Enter [0] to return to the previous menu")
            try:
                user_input = input("Select an option: ")
                option = int(user_input)
                if option not in (0, 1):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 0:
            return

        # update csv files
        users.loc[users['username'] == username, 'deactivation_requested'] = 0
        users.loc[users['username'] == username, 'active'] = status
        users.to_csv('users.csv', index=False)

        # increment or decrement number of volunteers if user has a camp
        if camp_name:
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
                vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
                vol_times.to_csv('volunteering_times.csv', index=False)

        print(username + "'s account has been " + change + "d successfully.")

        # while True:
        #     status = v.string("Would you like to deactivate or reactivate an user? (D/R)"
        #                       "\n D for deactivate"
        #                       "\n R for reactivate")
        #     if status != "R" and status != "D":
        #         print("Please enter only D or R.")
        #     elif status == "R":
        #         status = 1    #input this into the csv
        #         request = 0
        #         _str = "reactivate"
        #         break
        #     elif status == "D":
        #         status = 0
        #         _str = "deactivate"
        #         request = 0
        #         break
        #
        # df = pd.read_csv('users.csv', dtype={'password': str})
        # # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
        # print(df.iloc[1:, 0])
        # while True:
        #     user = v.string(f'Please enter the username you would like to {_str}. ')
        #     if any(df['username'].str.contains(user)) == False:  # testing if volunteer account already exists
        #         print("Username not found. Please enter again.")
        #     else:
        #         break
        # df.loc[df['username'] == user, 'deactivation_requested'] = request  # modify the dataform
        # df.loc[df['username'] == user, 'active'] = status
        # df.to_csv('users.csv', index=False)  # write it into the .csv file
        #
        # # update files for camps and volunteering sessions
        # # users = pd.read_csv('users.csv', dtype={'password': str})
        # cur_user = df[df['username'] == user]
        # cur_user = cur_user.replace({np.nan: None})
        # camp_name = cur_user.iloc[0]['camp_name']
        # # increment or decrement number of volunteers if user has a camp
        # if camp_name:
        #     plan_id = cur_user.iloc[0]['plan_id']
        #     camps = pd.read_csv(plan_id + '.csv')
        #     user_camp = (camps['camp_name'] == camp_name)
        #     if status == 1:
        #         camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] + 1
        #         camps.to_csv(plan_id + '.csv', index=False)
        #     if status == 0:
        #         camps.loc[user_camp, 'volunteers'] = camps.loc[user_camp, 'volunteers'] - 1
        #         camps.to_csv(plan_id + '.csv', index=False)
        #         # if deactivated: delete the user's volunteering sessions
        #         vol_times = pd.read_csv("volunteering_times.csv")
        #         vol_times = vol_times.drop(vol_times[vol_times['username'] == user].index)
        #         vol_times.to_csv('volunteering_times.csv', index=False)
        #
        # print(f'Complete. {user} is now modified.'
        #       "All status below:")
        # print(df)
        # logging.info({f'Admin has {_str}d {user}'})

    def low_resources_notification(self):

        # Getting the plan_id of all the plans created
        humani_plan = pd.read_csv('humanitarian_plan.csv')
        plans = []
        for index, row in humani_plan.iterrows():
            plans.append(row["plan_id"])
        # print(plans)

        for plan_id in plans:  # iterate through each humanitarian plan created
            current_plan = pd.read_csv(f'{plan_id}.csv')
            nb_of_camps = 0  # number of camps with low resources

            for i in current_plan.index:  # iterate through each camp of the current humanitarian plan
                refugees = current_plan.loc[i, "refugees"]
                camp = current_plan.loc[i, "camp_name"]
                food_left = refugees * 2 - current_plan.loc[i, "food"]
                water_left = refugees * 2 - current_plan.loc[i, "water"]
                firstaid_left = int((refugees * 2) / 3) - current_plan.loc[i, "firstaid_kits"]

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

    def resource_request_notification(self):
        try:
            requests = pd.read_csv('resource_requests.csv')
        except FileNotFoundError:
            return False # returns nothing if no new requests
        else:
            # if no new requests have been made, the column 'resolved' should only contain 'yes' values
            nb_of_requests = len(requests[requests["resolved"] == 'no'])
            if nb_of_requests == 0:
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

        requests = self.resource_request_notification()
        if requests is not False:  # if method above didn't return false
            new_requests = requests[requests["resolved"] == 'no']
            for index, row in new_requests.iterrows():
                user = row["username"]
                plan = row["plan_id"]
                camp = row["camp_name"]
                food_request = row["food"]
                water_request = row["water"]
                kit_request = row["firstaid_kits"]

                # Food requests
                while True:
                    option = v.string("\nEnter [C] to continue, or [X] to return to the previous menu: ")
                    if option.upper() == "X":
                        return
                    elif option.upper() == "C":
                        if food_request == 0:
                            print('\nNo requests for food.')
                            break
                        self.resource_request_processing(food_request, 'food', user, camp, plan)
                        break
                    else:
                        print("Please enter either [C] or [X].")

                # Water requests
                while True:
                    option = v.string("\nEnter [C] to continue, or [X] to return to the previous menu: ")
                    if option.upper() == "X":
                        return
                    elif option.upper() == "C":
                        if water_request == 0:
                            print('\nNo requests for water.')
                            break
                        self.resource_request_processing(water_request, 'water', user, camp, plan)
                        break
                    else:
                        print("Please enter either [C] or [X].")

                # First-aid kit requests
                while True:
                    option = v.string("\nEnter [C] to continue, or [X] to return to the previous menu: ")
                    if option.upper() == "X":
                        return
                    elif option.upper() == "C":
                        if kit_request == 0:
                            print('No requests for first-aid kits.')
                            break
                        self.resource_request_processing(kit_request, 'fofirstaid_kits', user, camp, plan)
                        break
                    else:
                        print("Please enter either [C] or [X]")

                # Marking that request as resolved
                requests.loc[index, "resolved"] = 'yes'

            # Saves to csv after iterating through all the new requests and marking them as resolved.
            requests.to_csv('resource_requests.csv', index=False)


    def resource_request_processing(self, requested_nb, resource, user, camp, plan):
        """
        This method is called when a request for more resources has been made by a volunteer.
        The admin uses the method to either accept or decline the request, updating the storage and
        camp resources accordingly.
        """
        resources_df = pd.read_csv(f'{plan}.csv')
        humani_plan_df = pd.read_csv("humanitarian_plan.csv")
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
                return

            while True:
                print('Enter [1] to approve their request')
                print('Enter [2] to decline their request')
                try:
                    option = int(input("Select an option: \n"))
                    if option not in (1, 2):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break
            if option == 1:
                print('Request accepted')
                humani_plan_df.loc[humani_plan_df.plan_id == plan, f'{resource}_storage'] -= requested_nb
                humani_plan_df.to_csv('humanitarian_plan.csv', index=False)
                resources_df.loc[resources_df.camp_name == camp, resource] += requested_nb
                resources_df.to_csv(f'{plan}.csv', index=False)
                print(f'The {resource} units for {camp} have increased by: {requested_nb}')
                print('This request has been marked as resolved.')
            elif option == 2:
                print('Request declined: no resource has been reallocated.')
                print('This request has been marked as resolved.')

    def deactivation_request_notification(self):
        """
        This method is used to notify the Admin if any new requests for deactivation have been made.
        If no new requests made, the method returns False.
        If one or more request has been made, the users dataframe is returned.
        The users dataframe is created from the users.csv file.
        """

        users = pd.read_csv('users.csv', dtype={'password': str})
        nb_of_requests = len(users[users["deactivation_requested"] == 1])
        if nb_of_requests == 0:
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
        users = self.deactivation_request_notification()
        if users is False:
            print("\nYou have not received no deactivation requests.")
            print("Returning to previous menu\n")
            return
        print("\nRespond to deactivation requests")
        nb_of_requests = len(users[users["deactivation_requested"] == 1])

        if nb_of_requests == 1:

            # extracts the username of the user who requested deactivation
            user_deactivating = users.loc[users['deactivation_requested'] == 1, 'username'].item()

            # calls method to deactivate the account
            self.deactivate_account_request(df=users, user=user_deactivating)

            # saves changes to the users.csv file
            users.to_csv('users.csv', index=False)
            print('The deactivation request has been processed!')
            return

        else:

            # extracts the usernames of users that requested deactivation into a list
            users_deactivating = users.loc[users['deactivation_requested'] == 1, 'username'].tolist()

            # calls the deactivation method for each username in the list
            for username in users_deactivating:
                self.deactivate_account_request(df=users, user=username)

            # saves the changes to the list
            users.to_csv('users.csv', index=False)
            print('All deactivation requests have been processed!')
            return

    def deactivate_account_request(self, df, user):
        """This method is called when an Admin wants to deactivate a volunteer's account following a request"""
        while True:
            print(f'\nUser {user} has requested to deactivate their account.\n')
            print('Enter [1] to deactivate {user}')
            print('Enter [2] to keep {user} active')
            print('Enter [0] to ignore this request for now.')
            try:
                option = int(input("Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break

        if option == 0:  # admin chose to ignore this request
            return

        elif option == 1: # admin chose to deactivate account
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

        else: # admin chose to keep account active
            df.loc[df['username'] == user, 'deactivation_requested'] = 0
            print(f'You have declined this request. {user} will remain active.')
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
            if end_date == "0":  # return to plan selection
                continue
            break

        # update csv files: add end date; remove volunteer accounts and volunteering sessions for that plan
        plans = pd.read_csv('humanitarian_plan.csv')
        plans = plans.replace({np.nan: None})
        plans.loc[plan_num - 1, 'end_date'] = end_date
        plan_id = plans['plan_id'].iloc[plan_num - 1]
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
        print(f"\nCurrently, the resources in storage are as follows:"
              f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
        print(f"And the resources in {hum_plan[:-4]} are as follows:"
              f"\n{resources.to_string(index=False)}")
        camp_format = False
        while camp_format == False:
            camp_no = v.integer("\nEnter [0] to return to the previous menu."
                                "\nEnter the number of the camp to which you would like to allocate resources: ")
            if camp_no == 0:
                return
            if any(resources['camp_name'].str.contains(f"Camp {camp_no}")):
                camp_format = True
            else:
                print('Please enter the number of an existing camp in this humanitarian plan.')

        # loop allows multiple resources to be allocated without re-selecting camp
        while True:
            print("\nChoose the resource you would like to allocate to Camp", camp_no, "of plan", hum_plan[:-4] + ".")
            print("Enter [1] for food packets")
            print("Enter [2] for water portions")
            print("Enter [3] for first-aid kits")
            print("Enter [0] to finish and return to the previous menu")
            try:
                resource_choice = int(input('Select an option: '))
                if resource_choice not in range(4):
                    raise ValueError
            except ValueError:
                logging.error('ValueError raised from user input')
                print('Please enter a number from the options provided.')
                continue
            if resource_choice == 0:
                resources.to_csv(hum_plan, index=False)
                humani_plan.to_csv("humanitarian_plan.csv", index=False)
                print(f"\nReturning to admin resources menu."
                      f"\nThe resources in {hum_plan[:-4]} are as follows:"
                      f"\n{resources}")
                print(f"\nAnd the remaining resources in storage: "
                      f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}")
                return
            if resource_choice == 1:
                while True:
                    print("\nEnter [B] to go back to the previous step.")
                    amount = input(f'Enter the number of food packets you would like to allocate to Camp {camp_no}: ')
                    if amount == "B":
                        break
                    try:
                        amount = int(amount)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("Please enter a positive integer.")
                        continue
                    # making sure number of {resource} entered does not exceed number in storage
                    in_storage = humani_plan.loc[humani_plan['location'] == location, 'food_storage']
                    if any(in_storage - amount < 0):
                        print('The amount entered exceeds the amount available in storage.'
                              '\nPlease check the amount in storage and try again.')
                    else:
                        humani_plan.loc[humani_plan['location'] == location, 'food_storage'] -= int(amount)
                        resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'food'] += int(
                            amount)  # like a = a + food
                        print("Allocation complete.")
                        break
            if resource_choice == 2:
                while True:
                    print("\nEnter [B] to go back to the previous step.")
                    amount = input(f'Enter the number of water portions you would like to allocate to Camp {camp_no}: ')
                    if amount == "B":
                        break
                    try:
                        amount = int(amount)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("Please enter a positive integer.")
                        continue
                    in_storage = humani_plan.loc[humani_plan['location'] == location, 'water_storage']
                    if any(in_storage - amount < 0):
                        print('The amount entered exceeds the amount available in storage.'
                              '\nPlease check the amount in storage and try again.')
                    else:
                        humani_plan.loc[humani_plan['location'] == location, 'water_storage'] -= int(amount)
                        resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'water'] += int(
                            amount)  # like a = a + food
                        print("Allocation complete.")
                        break
            if resource_choice == 3:
                while True:
                    print("\nEnter [B] to go back to the previous step.")
                    amount = input(f'Enter the number of first-aid kits you would like to allocate to Camp {camp_no}: ')
                    if amount == "B":
                        break
                    try:
                        amount = int(amount)
                        if amount <= 0:
                            raise ValueError
                    except ValueError:
                        print("Please enter a positive integer.")
                        continue
                    in_storage = humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage']
                    if any(in_storage - amount < 0):
                        print('The amount entered exceeds the amount available in storage.'
                              '\nPlease check the amount in storage and try again.')
                    else:
                        humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'] -= int(amount)
                        resources.loc[resources['camp_name'] == f"Camp {camp_no}", 'firstaid_kits'] += int(
                            amount)  # like a = a + food
                        print("Allocation complete.")
                        break


    def admin_menu(self):
        while self.logged_in:
            print("\n---------------")
            print("Admin Menu")
            print("---------------")
            self.deactivation_request_notification()
            self.resource_request_notification()
            self.low_resources_notification()
            while True:
                print("\nChoose would you would like to do.")
                print("Enter [1] to create, display, edit or end a humanitarian plan")
                print("Enter [2] to manage volunteer accounts (including camp identification)")
                print("Enter [3] to display, allocate or respond to requests for resources")
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
                print("Enter [3] to edit a humanitarian plan (i.e. description, no. of camps)")
                print("Enter [4] to update a camp's capacity")
                print("Enter [5] to end a humanitarian plan")
                print("Enter [0] to return to the admin menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    logging.debug(f'Admin has entered {user_input}.')
                    if option not in range(6):
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
        while True:
            print("\nManage Volunteer Accounts")
            while True:
                print("Enter [1] to create a volunteer account")
                print("Enter [2] to view a volunteer's details")
                print("Enter [3] to edit a volunteer's details")
                print("Enter [4] to update a volunteer's camp identification")
                print("Enter [5] to deactivate or reactivate a volunteer account")
                print("Enter [6] to respond to deactivation requests from volunteers")
                print("Enter [7] to delete a volunteer account")
                print("Enter [0] to return to the admin menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    logging.debug(f'Admin has entered {user_input}.')
                    if option not in range(8):
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
                logging.debug(f"Admin has chosen to respond to deactivation requests from volunteers.")
                self.check_deactivation_requests()
            if option == 7:
                logging.debug(f"Admin has chosen to delete a volunteer account.")
                self.delete_volunteer()

    def resources_menu(self):
        while True:
            print("\nManage Resources")
            while True:
                print("Enter [1] to display resources for a humanitarian plan")
                print("Enter [2] to manually allocate resources to camps in a humanitarian plan")
                print("Enter [3] to use auto-allocating feature")
                print("Enter [4] to respond to resource requests from volunteers")
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
                logging.debug(f"Admin has chosen to display resources.")
                print("\nDisplay resources")
                plan_id = select_plan()
                if plan_id == 0:
                    continue
                plan_csv = plan_id + ".csv"
                print(f"\nopening {plan_csv}...\n")
                self.display_resources(plan_csv)
                # humani_plan = pd.read_csv('humanitarian_plan.csv')
                # while True:
                #      try:
                #          print(humani_plan)
                #          index = v.integer(
                #              "Please enter the index of the humanitarian plan of which you would like to display resources.")
                #          location = humani_plan.loc[index, 'location'].replace(' ', '_')
                #          year = humani_plan.loc[index,'start_date'].split('-')[2]
                #          plan_csv = f"{location}_{year}.csv"
                #          print(f"\nopening {plan_csv}...\n")
                #          self.display_resources(plan_csv)
                #          break
                #      except KeyError:
                #          print("Please enter a correct index.")
            if option == 2:
                logging.debug(f"Admin has chosen to allocate resources manually.")
                print("\nManually allocate resources")
                plan_id = select_plan()
                if plan_id == 0:
                    continue
                hum_plan = plan_id + ".csv"
                location = plan_id[:-5]
                # humani_plan = pd.read_csv('humanitarian_plan.csv')
                # while True:
                #     try:
                #         print(humani_plan)
                #         index = v.integer(
                #             "Please enter the index of the humanitarian plan which you would like to allocate resources to.")
                #         location = humani_plan.loc[index, 'location'].replace(' ', '_')
                #         year = humani_plan.loc[index, 'start_date'].split('-')[2]
                #         hum_plan = f"{location}_{year}.csv"
                #         print(f"\nopening {hum_plan}...\n")
                #         break
                #     except KeyError:
                #         print("Please enter a correct index.")
                self.allocate_resources(hum_plan, location)
            if option == 3:  # auto-allocate
                logging.debug(f"Admin has chosen to auto-allocate resources.")
                print("\nAuto-allocate resources")
                plan_id = select_plan()
                if plan_id == 0:
                    continue
                hum_plan = plan_id + ".csv"
                location = plan_id[:-5]
                # humani_plan = pd.read_csv('humanitarian_plan.csv')
                # while True:
                #     print(humani_plan)
                #     index = v.integer(
                #         "Please enter the index of the humanitarian plan which you would like to allocate resources to.")
                #     if index not in humani_plan.index:
                #         print("Please enter a correct index.")
                #     else:
                #         location = humani_plan.loc[index, 'location'].replace(' ', '_')
                #         year = humani_plan.loc[index, 'start_date'].split('-')[2]
                #         hum_plan = f"{location}_{year}.csv"
                #         print(f"\nopening {hum_plan}...\n")
                #         break
                print(f"\nYou have selected {plan_id}.\n")
                print("\nWould you like to auto-allocate resources to all camps or select a camp?")
                print("Auto-allocating feature will top up resources to all camps for the following 7 days.")
                print("Enter [1] to allocate resources to all camps")
                print("Enter [2] to allocate resources to a specific camp")
                print("Enter [0] to return to the previous menu")
                while True:
                    option = v.integer("Select an option: ")
                    if option not in range(3):
                        print("Please enter a number from the options provided.")
                        continue
                    break
                if option == 1:
                    auto_resources.auto_all(hum_plan, location)
                if option == 2:
                    auto_resources.auto_one(hum_plan, location)
            if option == 4:
                logging.debug(f"Admin has chosen to respond to resource requests.")
                self.resource_request_menu()

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
            print("\nManage Volunteering Sessions")
            users = pd.read_csv('users.csv')
            users = users[(users['account_type'] == "volunteer") & (users['active'] == 1)]
            if len(users.index) == 0:
                print("There are no active volunteer accounts.")
                return

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
        print("You are now logged out. See you again!\n")

    def display_hum_plan(self):
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

    def update_camp_capacity(self):
        print("\nUpdate camp capacity")
        print("Select the camp whose capacity you would like to update.")
        progress = 0
        while progress < 3:
            if progress == 0:
                plan_id = select_plan()
                if plan_id == 0:
                    return
                else:
                    progress += 1

            if progress == 1:
                camp_name = select_camp(plan_id)
                if camp_name == "X":
                    # return
                    exit()
                elif camp_name == "B":
                    progress -= 1
                else:
                    progress += 1

            if progress == 2:
                camps = pd.read_csv(plan_id + ".csv")
                cur_camp = camps[camps['camp_name'] == camp_name]
                print("\nCurrent capacity of " + camp_name + ": " + str(cur_camp.iloc[0]['capacity']))
                print("The camp currently has " + str(cur_camp.iloc[0]['refugees']) + " refugees.")
                while True:
                    print("\nEnter [X] to return to the previous menu or [B] to go back to camp selection.")
                    new_capacity = input("New capacity: ")
                    if new_capacity == "X":
                        return
                    if new_capacity == "B":
                        progress -= 1
                        break
                    try:
                        new_capacity = int(new_capacity)
                        if new_capacity < 1:
                            raise ValueError
                    except ValueError:
                        print("Please enter a positive integer.")
                        continue
                    if new_capacity < cur_camp.iloc[0]['refugees']:
                        print(
                            "Invalid input: New capacity is less than refugee population. Please try again or return to the previous menu.")
                        continue
                    if new_capacity == cur_camp.iloc[0]['capacity']:
                        print("Capacity is unchanged. Please try again or return to the previous step.")
                        continue
                    progress += 1
                    break

        # update csv file
        chosen = (camps['camp_name'] == camp_name)
        camps.loc[chosen, 'capacity'] = new_capacity
        camps.to_csv(plan_id + '.csv', index=False)
        print("You have updated the capacity of", plan_id + ",", camp_name, "to", str(new_capacity) + ".")

    def view_volunteer(self):
        print("\nView volunteer details")
        print("Select the volunteer whose details you are viewing.")
        selected = select_plan_camp_vol(active=0, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            username = selected[2]

        users = pd.read_csv('users.csv', dtype={'password': str})
        select_user = users[users['username'] == username]
        select_user = select_user.replace({np.nan: None})
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
        print("Select the volunteer whose camp identification you are updating.")
        selected = select_plan_camp_vol(active=1, none=1)  # returns (plan_id, camp_name, username)
        if selected == 0:
            return
        else:
            plan_id, camp_name, username = selected

        def add_camp(plan_id):
            camps = pd.read_csv(plan_id + '.csv')
            print(username, "currently has no camp identification.")
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
            print(username + "'s current camp is:", camp_name)
            if len(camps.index) == 1:
                print("There is currently only one camp. It is not possible to change camp identification.")
                return camp_name

            while True:
                print("\nEnter [X] to return to the previous menu.")
                print("Choose a new camp.")
                print("Camp Name - # Volunteers - # Refugees - Capacity")
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
                print("\nEnter [1] to update camp identification")
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
                            print("Please enter a number from the options provided.")
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

            if camp_name and not new_camp:  # remove volunteering sessions
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times = vol_times.drop(vol_times[vol_times['username'] == username].index)
                vol_times.to_csv('volunteering_times.csv', index=False)
            if camp_name and new_camp:  # change camp_name in volunteering_times.csv
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
                camp_name = select_camp(plan_id)
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
        print("Select the refugee whose profile you are viewing.")
        selected = select_plan_camp_refugee()  # returns (plan_id, camp_name, refugee_id)
        if selected == 0:
            return
        else:
            plan_id, camp_name, refugee_id = selected

        refugees = pd.read_csv('refugees.csv')
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
        print("\nEdit or remove refugee profile")
        print("Select the refugee whose profile you would like to edit.")
        selected = select_plan_camp_refugee()  # returns (plan_id, camp_name, refugee_id)
        if selected == 0:
            return
        else:
            plan_id, camp_name, refugee_id = selected

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
                    if option not in (0, 1, 2, 3, 4, 5, 6, 9):
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
        selected = select_plan_camp_vol(active=1, none=0)
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
        selected = select_plan_camp_vol(active=1, none=0)
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
            print(str(row + 1) + ".", "Start:",
                  datetime.strptime(cur_user_times['start_time'].iloc[row], "%Y-%m-%d %H:%M").strftime(
                      "%d-%m-%Y %H:%M"),
                  "\t", "End:",
                  datetime.strptime(cur_user_times['end_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"))
        return

    def remove_volunteering_session(self):
        print("\nRemove a volunteering session")
        print("Select the volunteer for whom you are removing a session.")
        selected = select_plan_camp_vol(active=1, none=0)
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
                start = datetime.strptime(cur_user_times['start_time'].iloc[row], '%Y-%m-%d %H:%M').strftime(
                    '%d-%m-%Y %H:%M')
                end = datetime.strptime(cur_user_times['end_time'].iloc[row], '%Y-%m-%d %H:%M').strftime(
                    '%d-%m-%Y %H:%M')
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
            start = datetime.strptime(cur_user_times['start_time'].iloc[remove - 1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            end = datetime.strptime(cur_user_times['end_time'].iloc[remove - 1], '%Y-%m-%d %H:%M').strftime(
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
                                                 (vol_times['start_time'] == cur_user_times['start_time'].iloc[
                                                     remove - 1])].index)
            vol_times.to_csv('volunteering_times.csv', index=False)
            print("Volunteering session has been removed.")
            return
