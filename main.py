'''Run this file in the command line to open the application.'''
import pandas as pd, numpy as np, re, datetime
import logging
import volunteer_funcs
from volunteer import Volunteer
from coded_vars import convert_gender
from admin import Admin

logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    filemode='w',
                    format='%(module)s - %(levelname)s - %(message)s')


def main_menu():
    while True:
        logging.debug("User has entered main menu.")
        print("Main menu: Please login.")
        print("Enter [1] for Admin")
        print("Enter [2] for Volunteer")
        print("Enter [0] to exit the application")
        try:
            login_option = int(input("Select an option: "))
            if login_option not in (0, 1, 2):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.\n")
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
    print("\n-----------------")
    print("Admin Login")
    while True:
        logging.debug("User has entered admin login.")
        username = input("Username (enter 0 to go back): ")
        if username == "0":
            print("")
            return
        elif username == "":
            print("Please enter a username.")
            logging.warning("User did not enter a username.")
            continue
        password = input("Password (enter 0 to go back): ")
        if password == "0":
            continue

        # check login details against users table
        users = pd.read_csv('users.csv', dtype={'password': str})

        select_user = users[(users['username'] == username) & (users['account_type'] == "admin")]
        if len(select_user.index) == 0:  # username not registered
            print("Username not found. Please try again.\n")
            logging.warning("Username entered by user was not found.")
            continue

        if select_user.iloc[0]['password'] != password:  # password incorrect
            print("Incorrect password. Please try again.\n")
            logging.warning("User entered incorrect password.")
            continue

        print("Login successful!")
        logging.info("User logged in as: Admin")
        # create admin object
        a = Admin(username, password)
        a.admin_menu()
        return


def main_menu_vol():
    while True:
        logging.debug("User has entered main menu preceding volunteer login.")
        print("\nEnter [1] to register as a new volunteer")
        print("Enter [2] to login as Volunteer")
        print("Enter [0] to return to main menu")
        try:
            login_option_vol = int(input("Select an option: "))
            if login_option_vol not in (0, 1, 2):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue

        if login_option_vol == 0:
            print("")
            return
        elif login_option_vol == 1:
            volunteer_registration()
        else:  # login_option == 2
            volunteer_login()


def volunteer_login():
    print("\nVolunteer Login")
    while True:
        logging.debug("User has entered volunteer login.")
        username = input("Username (enter 0 to go back): ")
        if username == "0":
            return
        elif username.strip() == "":
            print("Please enter a username.")
            logging.warning("User did not enter a username.")
            continue
        password = input("Password (enter 0 to go back): ")
        if password == "0":
            continue

        # check login details against users table
        users = pd.read_csv('users.csv', dtype={'password': str})

        select_user = users[(users['username'] == username) & (users['account_type'] == "volunteer")]
        if len(select_user.index) == 0:  # username not registered
            print("Username not found. Please try again.\n")
            logging.warning("Username entered by user was not found.")
            continue

        if select_user.iloc[0]['password'] != password:  # password incorrect
            print("Incorrect password. Please try again.\n")
            logging.warning("User entered incorrect password.")
            continue

        if select_user.iloc[0]['active'] == 0:  # user has been deactivated
            print("Your account has been deactivated. Please contact system administrator.\n")
            logging.warning("User attempted to login but account is deactivated.")
            return

        # Login successful, initialise volunteer object and go to volunteer menu
        print("Login successful!")
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
    logging.debug("User has entered volunteer registration.")
    print("\nVolunteer Registration")
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

    users = pd.read_csv('users.csv', dtype={'password': str})
    new_row = {'username': [username], 'password': [password], 'account_type': ['volunteer'], 'active': [1],
               'deactivation_requested': [0], 'first_name': [first_name], 'last_name': [last_name], 'email': [email],
               'phone_number': [phone_number], 'gender': [gender], 'date_of_birth': [date_of_birth],
               'plan_id': [plan_id], 'camp_name': [camp_name]}
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
print("-----------------")
print("Welcome to the Humanitarian Management System")
print("-----------------")
main_menu()
