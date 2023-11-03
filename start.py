'''Run this file in the command line to open the application'''
import exceptions
import pandas as pd
import re
import datetime

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
            continue

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
            continue

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
    # Add to users file: email, phone_number, gender, DOB, camp
    print("\nVolunteer Registration")
    print("You will be prompted to enter details for registration.")

    def add_username():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            username = input("Enter username: ")
            if username in ("0", "9"):
                return username
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
            return username

    def add_password():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            password = input("Enter password: ") # use 111 for demonstration
            if password in ("0", "9"):
                return password
            # validation
            if password.strip() == "":
                print("Please enter a password.")
                continue
            if len(password) < 3:
                print("Password should be at least 3 characters.")
                continue
            return password

    def add_first_name():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            first_name = input("Enter first name: ")
            if first_name in ("0", "9"):
                return first_name
            # validation
            if first_name.strip() == "":
                print("Please enter a first name.")
                continue
            s = re.search("^[A-Z][a-zA-Z-' ]*$", first_name)
            if not s:
                print("First name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
                continue
            return first_name

    def add_last_name():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            last_name = input("Enter last name: ")
            if last_name in ("0", "9"):
                return last_name
            # validation
            if last_name.strip() == "":
                print("Please enter a last name.")
                continue
            s = re.search("^[a-zA-Z-' ]+$", last_name)
            if not s:
                print("Last name can only contain letters, hyphen (-) and apostrophe (').")
                continue
            return last_name

    def add_gender():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            print("Gender:")
            print("Enter [1] for male")
            print("Enter [2] for female")
            print("Enter [3] for non-binary")
            try:
                gender = int(input("Select an option: "))
                if gender not in (0, 1, 2, 3, 9):
                    raise exceptions.SelectOptionException
            except ValueError:
                print("Please enter a number from the options provided.\n")
                continue
            except exceptions.SelectOptionException:
                print("Please enter a number from the options provided.\n")
                continue
            return gender

    def add_dob():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            date_of_birth = input("Enter your date of birth in the format YYYY-MM-DD: ")
            if date_of_birth in ("0", "9"):
                return date_of_birth
            try:
                dob = datetime.date.fromisoformat(date_of_birth)
            except ValueError:
                print("Incorrect date format. Please use the format YYYY-MM-DD (e.g. 1999-07-23).")
                continue
            t = datetime.date.today()
            if dob > t:
                print("Date of birth cannot be in the future. Please try again.")
                continue
            if t.year - dob.year < 18 or (t.year - dob.year == 18 and t.month < dob.month) or (t.year - dob.year == 18 and t.month == dob.month and t.day < dob.day):
                print("Volunteers must be at least 18 years old.")
                invalid_age_option() # allows user to exit if they are ineligible
                continue
            if t.year - dob.year > 100 or (t.year - dob.year == 100 and t.month > dob.month) or (t.year - dob.year == 100 and t.month == dob.month and t.day >= dob.day):
                print("Volunteers must be 18-99 years old (inclusive).")
                invalid_age_option()
                continue
            return date_of_birth

    def invalid_age_option():
        while True:
            print("Enter [0] to re-enter date of birth")
            print("Enter [1] to exit the application")
            try:
                opt = int(input("Select an option: "))
                if opt not in (0, 1):
                    raise exceptions.SelectOptionException
            except ValueError:
                print("Please enter a number from the options provided.\n")
                continue
            except exceptions.SelectOptionException:
                print("Please enter a number from the options provided.\n")
                continue
            if opt == 0: return
            else:
                print("\nExiting the application.")
                print("Thank you for your interest in becoming a volunteer.\n")
                exit()

    def add_email():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            email = input("Enter email address: ")
            if email in ("0", "9"):
                return email
            # validation: email should be of the form "xxx@yyy.zzz"
            if email.strip() == "":
                print("Please enter an email address.")
                continue
            s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", email)
            if not s:
                print("Invalid email address. Please try again.")
                continue
            return email

    def add_phone_num():
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        while True:
            phone_num = input("Enter your phone number, including country code followed by a space (e.g. +44 07020123456): ")
            if phone_num in ("0", "9"):
                return phone_num
            s = re.search("^\+?\d{1,3} \d{8,11}$", phone_num) # allow starting + to be omitted
            if not s:
                print("Incorrect phone number format. Please try again.")
                continue
            if phone_num[0] != "+":
                phone_num = "+" + phone_num
            return phone_num

    def add_camp():
        plans = pd.read_csv('plans.csv')
        plans = plans[plans['end_date'].isna()]  # only show plans that haven't been closed

        if len(plans.index) == 0:
            print("No ongoing plans. Account will be created without camp identification.")
            return None

        camps = pd.read_csv('camps.csv')
        plans_camps = pd.merge(plans, camps, how="inner", on="plan_name")
        plans_camps = plans_camps[
            ['camp_name', 'plan_name', 'description', 'location', 'volunteers', 'refugees', 'capacity']]
        print("Enter [0] to return to the previous menu, [9] to go back to the previous step or [X] to proceed without camp identification.")

        while True:
            print("Choose a camp.")
            print(plans_camps)
            camp_name = input("Enter the name of the camp you would like to join: ")
            if camp_name in ("0", "9"):
                return camp_name
            elif camp_name == "X":
                return None

            if camp_name not in plans_camps['camp_name'].values:
                print("Please enter the name of a camp from the list displayed.\n")
                continue
            return camp_name


    progress = 0
    # loop allowing user to go back
    while progress < 9:
        if progress == 0:
            username = add_username()
            if username in ("0", "9"): break
            else: progress += 1

        elif progress == 1:
            password = add_password()
            if password == "0": break
            elif password == "9": progress -= 1
            else: progress += 1

        elif progress == 2:
            first_name = add_first_name()
            if first_name == "0": break
            elif first_name == "9": progress -= 1
            else: progress += 1

        elif progress == 3:
            last_name = add_last_name()
            if last_name == "0": break
            elif last_name == "9": progress -= 1
            else: progress += 1

        elif progress == 4:
            gender = add_gender()
            if gender == 0: break
            elif gender == 9: progress -= 1
            else: progress += 1

        elif progress == 5:
            date_of_birth = add_dob()
            if date_of_birth == "0": break
            elif date_of_birth == "9": progress -= 1
            else: progress += 1

        elif progress == 6:
            email = add_email()
            if email == "0": break
            elif email == "9": progress -= 1
            else: progress += 1

        elif progress == 7:
            phone_number = add_phone_num()
            if phone_number == "0": break
            elif phone_number == "9": progress -= 1
            else: progress += 1

        elif progress == 8:
            camp_name = add_camp()
            if camp_name == "0": break
            elif camp_name == "9": progress -= 1
            else: progress += 1

    # if exited loop before entering all details, it was to return to previous menu
    if progress < 9:
        volunteer_main_menu()

    # TODO: Update csv tables
    print("\nThank you for registering as a volunteer,", first_name, last_name, "!")
    print("Your details are as follows:")
    print("Username:", username)
    print("Email:", email)
    print("Phone number:", phone_number)
    print("Date of birth:", date_of_birth)
    print("Camp:", camp_name)
    print("You may now login to your account.")
    volunteer_main_menu()


# Run the program
print("-----------------")
print("Welcome to the Humanitarian Management System")
print("-----------------")
main_menu()
