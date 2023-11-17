import admin

'''Run this file in the command line to open the application.'''
import pandas as pd, numpy as np, re, datetime
import logging
from volunteer import Volunteer
from coded_vars import convert_gender
from admin import Admin

logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    filemode='w',
                    format='%(module)s - %(levelname)s - %(message)s')


def main_menu():
    while True:
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
            logging.error("ValueError raised from user input")
            continue

        if login_option == 0:
            print("\nExiting the application.")
            print("Thank you for using the Humanitarian Management System.\n")
            logging.info("User logged out.")
            exit()
        elif login_option == 1:
            admin_login()
        else:  # login_option == 2
            main_menu_vol()


def admin_login():
    print("\n-----------------")
    print("Admin Login")
    while True:
        username = input("Username (enter 0 to go back): ")
        if username == "0":
            print("")
            return
        elif username == "":
            print("Please enter a username.")
            continue
        password = input("Password (enter 0 to go back): ")
        if password == "0":
            continue

        # check login details against users table
        users = pd.read_csv('users.csv', dtype={'password': str})

        select_user = users[(users['username'] == username) & (users['account_type'] == "admin")]
        if len(select_user.index) == 0:  # username not registered
            print("Username not found. Please try again.\n")
            continue

        if select_user.iloc[0]['password'] != password:  # password incorrect
            print("Incorrect password. Please try again.\n")
            continue

        print("Login successful!")
        logging.info("User logged in as: Admin")
        # create admin object
        admin = Admin(username, password)
        admin.admin_menu()
        return


def main_menu_vol():
    while True:
        print("\nEnter [1] to register as a new volunteer")
        print("Enter [2] to login as Volunteer")
        print("Enter [0] to return to main menu")
        try:
            login_option_vol = int(input("Select an option: "))
            if login_option_vol not in (0, 1, 2):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.")
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
        username = input("Username (enter 0 to go back): ")
        if username == "0":
            return
        elif username.strip() == "":
            print("Please enter a username.")
            continue
        password = input("Password (enter 0 to go back): ")
        if password == "0":
            continue

        # check login details against users table
        users = pd.read_csv('users.csv', dtype={'password': str})

        select_user = users[(users['username'] == username) & (users['account_type'] == "volunteer")]
        if len(select_user.index) == 0:  # username not registered
            print("Username not found. Please try again.\n")
            continue

        if select_user.iloc[0]['password'] != password:  # password incorrect
            print("Incorrect password. Please try again.\n")
            continue

        if select_user.iloc[0]['active'] == 0:  # user has been deactivated
            print("Your account has been deactivated. Please contact system administrator.\n")
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
    print("\nVolunteer Registration")
    print("You will be prompted to enter details for registration.")

    def add_plan():
        plans = pd.read_csv('humanitarian_plan.csv')
        plans = plans[plans['end_date'].isna()]  # only show plans that haven't been closed

        if len(plans.index) == 0:
            print("\nThere are no ongoing humanitarian plans. Please check back later.")
            return "B"

        while True:
            print("\nEnter [B] to return to the previous menu.")
            print("Choose a plan.")
            print("\nNumber - Location - Event Description - Start Date - # Camps")
            for row in range(len(plans.index)):
                print(row + 1, plans['location'].iloc[row], plans['description'].iloc[row],
                      plans['start_date'].iloc[row], str(plans['number_of_camps'].iloc[row]) + " camps", sep=" - ")
            plan_num = input("Enter the number of the plan you would like to join: ")
            if plan_num == "B":
                return plan_num
            try:
                plan_num = int(plan_num)
                if plan_num not in range(1, len(plans.index) + 1):
                    raise ValueError
            except ValueError:
                logging.error("ValueError raised from user input")
                print("Please enter a number from the options provided.\n")
                continue
            break

        plan_id = plans['location'].iloc[plan_num - 1] + "_" + plans['start_date'].iloc[plan_num - 1][6:]
        print("Your plan ID is:", plan_id)
        return plan_id  # e.g. Australia_2023

    def add_camp(plan_id):
        camps = pd.read_csv(plan_id + '.csv')

        while True:
            print(
                "\nEnter [0] to return to the previous menu, [9] to go back to the previous step or [X] to proceed without camp identification.")
            print("Choose a camp.")
            print("\nCamp Name - # Volunteers - # Refugees - Capacity")
            for row in range(1, len(camps.index)):
                print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                      str(camps['refugees'].iloc[row]) + " refugees",
                      str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
            camp_name = input("Enter the name of the camp you would like to join: ")
            if camp_name in ("0", "9"):
                return camp_name
            elif camp_name == "X":
                return None

            if camp_name not in camps['camp_name'].values:
                print("Please enter the name of a camp from the list displayed.")
                continue

            print("You have chosen", camp_name + ".")
            return camp_name

    def add_username():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            username = input("Enter username: ").strip()
            if username in ("0", "9"):
                return username
            # validation
            if username == "":
                print("Please enter a username.")
                continue
            s = re.search("^[a-zA-Z]+[a-zA-Z0-9_]*$", username)
            if not s:
                print(
                    "Username can only contain letters, digits (0-9) and underscore (_), "
                    "and must start with a letter. Please choose another username.")
                continue
            users = pd.read_csv('users.csv', dtype={'password': str})
            select_username = users[users['username'] == username]
            if len(select_username.index) > 0:  # username already exists
                print("Username is taken. Please choose another username.")
                continue
            return username

    def add_password():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            password = input("Enter password: ")  # use 111 for demonstration
            if password in ("0", "9"):
                return password
            # validation
            if len(password) < 3:
                print("Password should be at least 3 characters.")
                continue
            s = re.search("[, ]", password)
            if s:
                print("Password cannot contain commas or spaces. Please choose another password.")
                continue
            return password

    def add_first_name():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            first_name = input("Enter first name: ").strip()
            if first_name in ("0", "9"):
                return first_name
            # validation
            if first_name == "":
                print("Please enter a first name.")
                continue
            s = re.search("^[A-Z][a-zA-Z-' ]*$", first_name)
            if not s:
                print(
                    "First name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
                continue
            return first_name

    def add_last_name():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            last_name = input("Enter last name: ").strip()
            if last_name in ("0", "9"):
                return last_name
            # validation
            if last_name == "":
                print("Please enter a last name.")
                continue
            s = re.search("^[a-zA-Z-' ]+$", last_name)
            if not s:
                print("Last name can only contain letters, hyphen (-) and apostrophe (').")
                continue
            return last_name

    def add_gender():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            print("Gender:")
            print("Enter [1] for male")
            print("Enter [2] for female")
            print("Enter [3] for non-binary")
            try:
                gender = int(input("Select an option: "))
                if gender not in (0, 1, 2, 3, 9):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.\n")
                continue
            return gender

    def add_dob():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            date_of_birth = input("Enter your date of birth in the format DD-MM-YYYY: ").strip()
            if date_of_birth in ("0", "9"):
                return date_of_birth
            try:
                dob = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date()
                # dob = datetime.date.fromisoformat(date_of_birth)
            except ValueError:
                print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
                continue
            t = datetime.date.today()
            if dob > t:
                print("Date of birth cannot be in the future. Please try again.")
                continue
            if t.year - dob.year < 18 or (t.year - dob.year == 18 and t.month < dob.month) or (
                    t.year - dob.year == 18 and t.month == dob.month and t.day < dob.day):
                print("Volunteers must be at least 18 years old.")
                invalid_age_option()  # allows user to exit if they are ineligible
                continue
            if t.year - dob.year > 100 or (t.year - dob.year == 100 and t.month > dob.month) or (
                    t.year - dob.year == 100 and t.month == dob.month and t.day >= dob.day):
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
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.\n")
                continue
            if opt == 0:
                return
            else:
                print("\nExiting the application.")
                print("Thank you for your interest in becoming a volunteer.\n")
                exit()

    def add_email():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            email = input("Enter email address: ").strip()
            if email in ("0", "9"):
                return email
            # validation: email should be of the form "xxx@yyy.zzz"
            if email == "":
                print("Please enter an email address.")
                continue
            s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", email)
            if not s:
                print("Invalid email address. Please try again.")
                continue
            return email

    def add_phone_num():
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            phone_num = input(
                "Enter your phone number, including country code followed by a space (e.g. +44 07020123456): ").strip()
            if phone_num in ("0", "9"):
                return phone_num
            if phone_num == "":
                print("Please enter a phone number.")
                continue
            s = re.search("^\+?\d{1,3} \d{8,11}$", phone_num)  # allow starting + to be omitted
            if not s:
                print("Incorrect phone number format. Please try again.")
                continue
            if phone_num[0] != "+":
                phone_num = "+" + phone_num
            return phone_num

    progress = 0
    # loop allowing user to go back
    while progress < 10:
        if progress == 0:
            plan_id = add_plan()
            if plan_id == "B":
                break
            else:
                progress += 1

        elif progress == 1:
            camp_name = add_camp(plan_id)
            if camp_name == "0":
                break
            elif camp_name == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 2:
            username = add_username()
            if username == "0":
                break
            elif username == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 3:
            password = add_password()
            if password == "0":
                break
            elif password == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 4:
            first_name = add_first_name()
            if first_name == "0":
                break
            elif first_name == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 5:
            last_name = add_last_name()
            if last_name == "0":
                break
            elif last_name == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 6:
            gender = add_gender()
            if gender == 0:
                break
            elif gender == 9:
                progress -= 1
            else:
                progress += 1

        elif progress == 7:
            date_of_birth = add_dob()
            if date_of_birth == "0":
                break
            elif date_of_birth == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 8:
            email = add_email()
            if email == "0":
                break
            elif email == "9":
                progress -= 1
            else:
                progress += 1

        elif progress == 9:
            phone_number = add_phone_num()
            if phone_number == "0":
                break
            elif phone_number == "9":
                progress -= 1
            else:
                progress += 1

    # if exited loop before entering all details, it was to return to previous menu
    if progress < 10:
        return

    # Update csv tables
    users = open("users.csv", "a")
    if camp_name:
        users.write(
            f'\n{username},{password},volunteer,1,0,{first_name},{last_name},{email},{phone_number},{gender},{date_of_birth},{plan_id},{camp_name}')
    else:
        users.write(
            f'\n{username},{password},volunteer,1,0,{first_name},{last_name},{email},{phone_number},{gender},{date_of_birth},{plan_id},')
    users.close()

    # users = pd.read_csv('users.csv', dtype={'password': str})
    # new_row = {'username': [username], 'password': [password], 'active': [1], 'first_name': [first_name],
    #            'last_name': [last_name], 'email': [email], 'phone_number': [phone_number], 'gender': [gender],
    #            'date_of_birth': [date_of_birth], 'camp_name': [camp_name]}
    # new = pd.DataFrame(new_row)
    # users = pd.concat([users, new], ignore_index=True)
    # users.to_csv('users.csv', index=False)

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
