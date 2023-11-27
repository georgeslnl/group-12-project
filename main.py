'''Run this file in the command line to open the application.'''
# built-in modules
import pandas as pd, numpy as np, datetime, os
import logging
# custom modules and functions from other files
from progs import volunteer_funcs
from progs.volunteer import Volunteer
from progs.admin import Admin
from progs.coded_vars import convert_gender

logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    filemode='w',
                    format='%(module)s - %(levelname)s - %(message)s')


def main_menu():
    """
    The main menu that runs when the application is first started.
    Gives the user options to login as an admin or volunteer (including volunteer registration).
    """
    while True:
        logging.debug("User has entered main menu.")
        print("--------------------------------------------")
        print("\t\tMAIN MENU")
        print("Please choose your user type.")
        print("Enter [1] for Admin")
        print("Enter [2] for Volunteer")
        print("Enter [0] to exit the application\n")
        try:
            login_option = int(input(">>Enter your option: "))
            if login_option not in (0, 1, 2):
                raise ValueError
        except ValueError:
            print("\nPlease enter a number from the options provided.\n")
            logging.error("Invalid user input.")
            continue

        if login_option == 0:
            print("\nExiting the application.")
            print("Thank you for using the Humanitarian Management System.\n")
            logging.info("User exited the application.")
            exit()
        elif login_option == 1:
            admin_login()
        else:  # login_option == 2
            main_menu_vol()


def admin_login():
    """
    Prompts the user to enter the admin's username and password.
    If the correct details are entered, an admin object is created and the user logs in as an admin.
    """
    print("\n--------------------------------------------")
    print("\t\tADMIN LOGIN")
    while True:
        logging.debug("User has entered admin login.")
        username = input(">>Username (enter [0] to go back to main menu): ")
        if username == "0":
            print("")
            return
        elif username == "":
            print("Please enter a username.")
            logging.warning("User did not enter a username.")
            continue
        password = input(">>Password (enter [0] to go back to username): ")
        if password == "0":
            continue

        # check login details against users table
        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})

        select_user = users[(users['username'] == username) & (users['account_type'] == "admin")]
        if len(select_user.index) == 0:  # username not registered
            print("\nUsername not found. Please try again.\n")
            logging.warning("Username entered by user was not found.")
            continue

        if select_user.iloc[0]['password'] != password:  # password incorrect
            print("\nIncorrect password. Please try again.\n")
            logging.warning("User entered incorrect password.")
            continue

        print("\nLogin successful!")
        logging.info("User logged in as: Admin")
        # create admin object
        a = Admin(username, password)
        a.admin_menu()
        return


def main_menu_vol():
    """
    This menu prompts the user to choose whether to login or register as a volunteer.
    """
    while True:
        logging.debug("User has entered main menu preceding volunteer login.")
        print("\n--------------------------------------------")
        print("\t\tVOLUNTEER")
        print("Enter [1] to register as a new volunteer")
        print("Enter [2] to login as Volunteer")
        print("Enter [0] to return to main menu\n")
        try:
            login_option_vol = int(input(">>Enter your option: "))
            if login_option_vol not in (0, 1, 2):
                raise ValueError
        except ValueError:
            print("\nPlease enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue

        if login_option_vol == 0:
            logging.debug("Returning to main menu.")
            print("")
            return
        elif login_option_vol == 1:
            volunteer_registration()
        else:  # login_option == 2
            volunteer_login()


def volunteer_login():
    """
    Prompts the user to enter their username and password to login as a volunteer.
    If the correct details are entered and the user's account is active, a volunteer object is created and the user logs in.
    If the correct details are entered but the user's account has been deactivated,
    the user is informed of this and returned to the previous menu.
    """
    print("\n--------------------------------------------")
    print("\t\tVOLUNTEER LOGIN")
    while True:
        logging.debug("User has entered volunteer login.")
        username = input(">>Username (enter [0] to go back to previous menu): ")
        if username == "0":
            return
        elif username.strip() == "":
            print("\nPlease enter a username.")
            logging.warning("User did not enter a username.")
            continue
        password = input(">>Password (enter [0] to go back to username): ")
        if password == "0":
            continue

        # check login details against users table
        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})

        select_user = users[(users['username'] == username) & (users['account_type'] == "volunteer")]
        if len(select_user.index) == 0:  # username not registered
            print("\nUsername not found. Please try again.\n")
            logging.warning("Username entered by user was not found.")
            continue

        if select_user.iloc[0]['password'] != password:  # password incorrect
            print("\nIncorrect password. Please try again.\n")
            logging.warning("User entered incorrect password.")
            continue

        if select_user.iloc[0]['active'] == 0:  # user has been deactivated
            print("\nYour account has been deactivated. Please contact system administrator.\n")
            logging.warning("User attempted to login but account is deactivated.")
            return

        # Login successful, initialise volunteer object and go to volunteer menu
        print("\nLogin successful!")
        logging.info("User logged in as: Volunteer")
        select_user = select_user.replace({np.nan: None})
        v = Volunteer(select_user.iloc[0]['username'], select_user.iloc[0]['password'],
                      select_user.iloc[0]['first_name'], select_user.iloc[0]['last_name'], select_user.iloc[0]['email'],
                      select_user.iloc[0]['phone_number'], select_user.iloc[0]['gender'],
                      select_user.iloc[0]['date_of_birth'], select_user.iloc[0]['plan_id'],
                      select_user.iloc[0]['camp_name'])
        v.volunteer_menu()
        # proceed only when user has logged out
        return


def volunteer_registration():
    """
    Enables the user to create a new volunteer account at a selected humanitarian plan.
    The user is prompted for their details one by one.
    """
    logging.debug("User has entered volunteer registration.")
    print("\n--------------------------------------------")
    print("\t\tVOLUNTEER REGISTRATION")
    print("You will be prompted to enter details for registration.")

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

    logging.debug("User has finished entering details for volunteer registration.")
    # Update csv files
    # users = open("users.csv", "a")
    # if camp_name:
    #     users.write(
    #         f'\n{username},{password},volunteer,1,0,{first_name},{last_name},{email},{phone_number},{gender},{date_of_birth},{plan_id},{camp_name}')
    # else:
    #     users.write(
    #         f'\n{username},{password},volunteer,1,0,{first_name},{last_name},{email},{phone_number},{gender},{date_of_birth},{plan_id},')
    # users.close()

    users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
    new_row = {'username': [username], 'password': [password], 'account_type': ['volunteer'], 'active': [1],
               'deactivation_requested': [0], 'first_name': [first_name], 'last_name': [last_name], 'email': [email],
               'phone_number': [phone_number], 'gender': [gender], 'date_of_birth': [date_of_birth],
               'plan_id': [plan_id], 'camp_name': [camp_name]}
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
    print("\nThank you for registering as a volunteer,", first_name, last_name + "!")
    print("Your details are as follows:")
    print("Plan:", plan_id)
    print("Camp:", camp_name)
    print("Username:", username)
    print("Email:", email)
    print("Phone number:", phone_number)
    print("Gender:", gender_str)
    print("Date of birth (DD-MM-YYYY):", date_of_birth)
    print("You may now login to your account.")
    return


# Run the program
print("---------------------------------------------------------------------")
print("│          ╦ ╦ ┬ ┬ ┌┬┐ ┌─┐ ┌┐┌ ┬ ┌┬┐ ┌─┐ ┬─┐ ┬ ┌─┐ ┌┐┌             │")
print("│          ╠═╣ │ │ │││ ├─┤ │││ │  │  ├─┤ ├┬┘ │ ├─┤ │││             │")
print("│          ╩ ╩ └─┘ ┴ ┴ ┴ ┴ ┘└┘ ┴  ┴  ┴ ┴ ┴└─ ┴ ┴ ┴ ┘└┘             │")
print("│ ╔╦╗ ┌─┐ ┌┐┌ ┌─┐ ┌─┐ ┌─┐ ┌┬┐ ┌─┐ ┌┐┌ ┌┬┐  ╔═╗ ┬ ┬ ┌─┐ ┌┬┐ ┌─┐ ┌┬┐ │")
print("│ ║║║ ├─┤ │││ ├─┤ │ ┬ ├┤  │││ ├┤  │││  │   ╚═╗ └┬┘ └─┐  │  ├┤  │││ │")
print("│ ╩ ╩ ┴ ┴ ┘└┘ ┴ ┴ └─┘ └─┘ ┴ ┴ └─┘ ┘└┘  ┴   ╚═╝  ┴  └─┘  ┴  └─┘ ┴ ┴ │")
print("│     Authors: Elsie BROWN, Georges LINEL, Jasmine CHAU,           │")
print("│              Matthew GOH, Victor CHAN, and Ying HUANG            │")
print("---------------------------------------------------------------------")
print("           WELCOME TO HUMANITARIAN MANAGEMENT SYSTEM!\n")

# When application starts, delete all volunteering sessions that ended in the past
vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
vol_times = vol_times.drop(vol_times[vol_times['end_time'] < n].index)
vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)

main_menu()
