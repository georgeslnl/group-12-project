'''Run this file in the command line to open the application'''

import exceptions
import pandas as pd
import re

def main_menu():
    while True:
        print("Main menu: Please login.")
        print("Enter [1] for Admin")
        print("Enter [2] for Volunteer")
        print("Enter [0] to exit the application")
        try:
            login_option = int(input("Select an option: "))
            if login_option not in (0, 1, 2):
                raise exceptions.SelectOptionException
        except ValueError:
            print("Please enter a number from the options provided.\n")
            continue
        except exceptions.SelectOptionException:
            print("Please enter a number from the options provided.\n")

        if login_option == 0:
            print("\nExiting the application.")
            print("Thank you for using the Humanitarian Management System.\n")
            exit()
        elif login_option == 1:
            admin_login()
        else:  # login_option == 2
            volunteer_main_menu()
        break

def admin_login():
    print("\n-----------------")
    print("Admin Login")
    while True:
        username = input("Username (enter 0 to go back): ")
        if username == "0":
            print("")
            main_menu()
        elif username == "":
            print("Please enter a username.")
            continue
        password = input("Password (enter 0 to go back): ")
        if password == "0":
            continue

        # check login details
        if username == "admin" and password == "111":
            # admin_menu()
            pass
        elif username != "admin":
            print("Username not found. Please try again.\n")
            continue
        else: # password != "111"
            print("Incorrect password. Please try again.\n")
            continue
        break

def volunteer_main_menu():
    print("\n-----------------")
    while True:
        print("Enter [1] to register as a new volunteer")
        print("Enter [2] to login as Volunteer")
        print("Enter [0] to return to main menu")
        try:
            login_option_vol = int(input("Select an option: "))
            if login_option_vol not in (0, 1, 2):
                raise exceptions.SelectOptionException
        except ValueError:
            print("Please enter a number from the options provided.\n")
            continue
        except exceptions.SelectOptionException:
            print("Please enter a number from the options provided.\n")

        if login_option_vol == 0:
            print("")
            main_menu()
        elif login_option_vol == 1:
            volunteer_registration()
        else:  # login_option == 2
            volunteer_login()
        break

def volunteer_login():
    print("\nVolunteer Login")
    while True:
        username = input("Username (enter 0 to go back): ")
        if username == "0":
            volunteer_main_menu()
        elif username.strip() == "":
            print("Please enter a username.")
            continue
        password = input("Password (enter 0 to go back): ")
        if password == "0":
            continue

        # check login details against users table
        user_details = pd.read_csv('users.csv', dtype={'password': str})
        # print(user_details)

        select_user = user_details[user_details['username'] == username]
        if len(select_user.index) == 0: # username not registered
            print("Username not found. Please try again.\n")
            continue

        select_user_password = select_user[select_user['password'] == password]
        if len(select_user_password.index) == 0: # password incorrect
            print("Incorrect password. Please try again.\n")
            continue

        # Login successful, go to volunteer menu
        print("Login successful!")
        # volunteer_menu()
        break

def volunteer_registration():
    # Add to users file: username, password, active, first_name, last_name, email, phone_number, address, gender, DOB, camp
    print("\nVolunteer Registration")
    print("You will be prompted to enter details for registration.")
    print("At any point, you may enter [0] to return to the previous menu or [9] to go back to the previous step.")
    # Username
    while True:
        username = input("Enter username: ")
        if username == "0":
            volunteer_main_menu()
        elif username == "9":
            volunteer_main_menu()
        # validation
        if username.strip() == "":
            print("Please enter a username.")
            continue
        s = re.search("^[a-zA-Z]+[a-zA-Z0-9_]*$", username)
        if not s:
            print("Username can only contain letters, digits (0-9) and underscore (_), and must start with a letter. Please choose another username.")
            continue
        user_details = pd.read_csv('users.csv', dtype={'password': str})
        select_username = user_details[user_details['username'] == username]
        if len(select_username.index) > 0:  # username already exists
            print("Username is taken. Please choose another username.")
            continue

        # Password
        while True:
            password = input("Enter password: ")
            if password == "0":
                volunteer_main_menu()
            elif password == "9":
                break
            # validation
            if password.strip() == "":
                print("Please enter a password.")
                continue

            # First name
            while True:
                first_name = input("Enter first name: ")
                if first_name == "0":
                    volunteer_main_menu()
                elif first_name == "9":
                    break
                # validation
                if first_name.strip() == "":
                    print("Please enter a first name.")
                    continue
                s = re.search("^[A-Z][a-zA-Z-' ]*$", first_name)
                if not s:
                    print("First name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
                    continue

                # Last name
                while True:
                    last_name = input("Enter last name: ")
                    if last_name == "0":
                        volunteer_main_menu()
                    elif last_name == "9":
                        break
                    # validation
                    if last_name.strip() == "":
                        print("Please enter a last name.")
                        continue
                    s = re.search("^[a-zA-Z-' ]+$", last_name)
                    if not s:
                        print(
                            "Last name can only contain letters, hyphen (-) and apostrophe (').")
                        continue

                    # Email
                    while True:
                        email = input("Enter email: ")
                        if email == "0":
                            volunteer_main_menu()
                        elif email == "9":
                            break
                        # validation
                        break


# Run the program
print("-----------------")
print("Welcome to the Humanitarian Management System")
print("-----------------")
main_menu()
