import pandas as pd, re, datetime
from coded_vars import convert_gender
import logging

def add_plan():
    """Prompts the user to select an ongoing humanitarian plan."""
    plans = pd.read_csv('humanitarian_plan.csv')
    plans = plans[plans['end_date'].isna()]  # only show plans that haven't been closed

    if len(plans.index) == 0:
        print("\nThere are no ongoing humanitarian plans. Please check back later.")
        logging.info("No ongoing humanitarian plans.")
        return "X"

    logging.debug("User prompted to select humanitarian plan.")
    while True:
        print("\nEnter [X] to return to the previous menu.")
        print("Choose a plan.")
        print("\nNumber - Location - Event Description - Start Date - # Camps")
        for row in range(len(plans.index)):
            print(row + 1, plans['location'].iloc[row], plans['description'].iloc[row],
                  plans['start_date'].iloc[row], str(plans['number_of_camps'].iloc[row]) + " camps", sep=" - ")
        plan_num = input("Enter the number of the plan you would like to join: ")
        if plan_num.upper() == "X":
            return plan_num.upper()
        try:
            plan_num = int(plan_num)
            if plan_num not in range(1, len(plans.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        break

    plan_id = plans['plan_id'].iloc[plan_num - 1]
    print("Your plan ID is:", plan_id)
    return plan_id  # e.g. London_2023


def add_camp(plan_id):
    """
    Takes as input the plan_id of an ongoing humanitarian plan.
    Prompts the user to select a camp at this plan.
    """
    camps = pd.read_csv(plan_id + '.csv')

    logging.debug("User prompted to select camp.")
    while True:
        print(
            "\nEnter [X] to return to the previous menu, [B] to go back to the previous step or [N] to proceed without camp identification.")
        print("Choose a camp.")
        print("Camp Name - # Volunteers - # Refugees - Capacity")
        for row in range(len(camps.index)):
            print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                  str(camps['refugees'].iloc[row]) + " refugees",
                  str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
        camp_num = input("Enter the number of the camp you would like to join (e.g. [1] for Camp 1): ")
        if camp_num.upper() in ("X", "B"):
            return camp_num.upper()
        elif camp_num.upper() == "N":
            return None
        try:
            camp_num = int(camp_num)
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter the number of a camp from the list displayed.")
            logging.error("Invalid user input.")
            continue

        camp_name = "Camp " + str(camp_num)
        print("You have chosen", camp_name + ".")
        return camp_name


def add_username():
    """Prompts the user to enter the volunteer's username."""
    logging.debug("User prompted to enter username.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        username = input("Enter username: ").strip()
        if username in ("0", "9"):
            return username
        # validation
        if username == "":
            print("Please enter a username.")
            logging.error("User did not enter a username.")
            continue
        s = re.search("^[a-zA-Z]+[a-zA-Z0-9_]*$", username)
        if not s:
            print(
                "Username can only contain letters, digits (0-9) and underscore (_), "
                "and must start with a letter. Please choose another username.")
            logging.error("Invalid user input.")
            continue
        users = pd.read_csv('users.csv', dtype={'password': str})
        select_username = users[users['username'] == username]
        if len(select_username.index) > 0:  # username already exists
            print("Username is taken. Please choose another username.")
            logging.error("User entered a username that already exists.")
            continue
        return username


def add_password():
    """Prompts the user to enter the volunteer's password."""
    logging.debug("User prompted to enter password.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        password = input("Enter password: ")  # use 111 for demonstration
        if password in ("0", "9"):
            return password
        # validation
        if len(password) < 3:
            print("Password should be at least 3 characters.")
            logging.error("Invalid user input.")
            continue
        s = re.search("[, ]", password)
        if s:
            print("Password cannot contain commas or spaces. Please choose another password.")
            logging.error("Invalid user input.")
            continue
        return password


def add_first_name():
    """Prompts the user to enter the volunteer's first name."""
    logging.debug("User prompted to enter first name.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        first_name = input("Enter first name: ").strip()
        if first_name in ("0", "9"):
            return first_name
        # validation
        if first_name == "":
            print("Please enter a first name.")
            logging.error("User did not enter a first name.")
            continue
        s = re.search("^[A-Z][a-zA-Z-' ]*$", first_name)
        if not s:
            print(
                "First name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
            logging.error("Invalid user input.")
            continue
        return first_name


def add_last_name():
    """Prompts the user to enter the volunteer's last name."""
    logging.debug("User prompted to enter last name.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        last_name = input("Enter last name: ").strip()
        if last_name in ("0", "9"):
            return last_name
        # validation
        if last_name == "":
            print("Please enter a last name.")
            logging.error("User did not enter a last name.")
            continue
        s = re.search("^[a-zA-Z-' ]+$", last_name)
        if not s:
            print("Last name can only contain letters, hyphen (-) and apostrophe (').")
            logging.error("Invalid user input.")
            continue
        return last_name


def add_gender():
    """Prompts the user to select the volunteer's gender."""
    logging.debug("User prompted to select gender.")
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
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        return gender


def add_dob():
    """
    Prompts the user to enter the volunteer's date of birth.
    If the volunteer is not aged 18-99, a warning is displayed and the user is given the option to re-enter the date of birth or leave the method.
    """
    logging.debug("User prompted to enter date of birth.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        date_of_birth = input("Enter your date of birth in the format DD-MM-YYYY: ").strip()
        if date_of_birth in ("0", "9"):
            return date_of_birth
        try:
            dob = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date()
        except ValueError:
            print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
            logging.error("Invalid user input.")
            continue
        t = datetime.date.today()
        if dob > t:
            print("Date of birth cannot be in the future. Please try again.")
            logging.error("User entered a date of birth in the future.")
            continue
        if t.year - dob.year < 18 or (t.year - dob.year == 18 and t.month < dob.month) or (
                t.year - dob.year == 18 and t.month == dob.month and t.day < dob.day):
            print("Volunteers must be at least 18 years old.")
            logging.warning("Volunteer is less than 18 years old based on date of birth.")
            opt = invalid_age_option()  # allows user to exit if they are ineligible
            if opt == 1:
                continue
            else: # opt == 0
                return "0"
        if t.year - dob.year > 100 or (t.year - dob.year == 100 and t.month > dob.month) or (
                t.year - dob.year == 100 and t.month == dob.month and t.day >= dob.day):
            print("Volunteers must be 18-99 years old (inclusive).")
            logging.warning("Volunteer is more than 99 years old based on date of birth.")
            opt = invalid_age_option()
            if opt == 1:
                continue
            else:  # opt == 0
                return "0"
        return date_of_birth


def invalid_age_option():
    """
    Called when the volunteer's age is not 18-99 when creating an account.
    The user is given the option to re-enter the date of birth or leave the method.
    """
    logging.debug("User prompted to choose whether to re-enter date of birth or return to previous menu.")
    while True:
        print("Enter [1] to re-enter date of birth")
        print("Enter [0] to return to the previous menu")
        try:
            opt = int(input("Select an option: "))
            if opt not in (0, 1):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.\n")
            logging.error("Invalid user input.")
            continue
        return opt


def add_email():
    """Prompts the user to enter the volunteer's email address."""
    logging.debug("User prompted to enter email address.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        email = input("Enter email address: ").strip()
        if email in ("0", "9"):
            return email
        # validation: email should be of the form "xxx@yyy.zzz"
        if email == "":
            print("Please enter an email address.")
            logging.error("User did not enter an email address.")
            continue
        s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", email)
        if not s:
            print("Invalid email address. Please try again.")
            logging.error("Invalid user input.")
            continue
        return email


def add_phone_num():
    """Prompts the user to enter the volunteer's phone number."""
    logging.debug("User prompted to enter phone number.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        phone_num = input(
            "Enter your phone number, including country code followed by a space (e.g. +44 07020123456): ").strip()
        if phone_num in ("0", "9"):
            return phone_num
        if phone_num == "":
            print("Please enter a phone number.")
            logging.error("User did not enter a phone number.")
            continue
        s = re.search("^\+?\d{1,3} \d{8,11}$", phone_num)  # allow starting + to be omitted
        if not s:
            print("Incorrect phone number format. Please try again.")
            logging.error("Invalid user input.")
            continue
        if phone_num[0] != "+":
            phone_num = "+" + phone_num
        return phone_num


##############################################
# Functions for admin to edit volunteer details
def edit_username(username):
    """Prompts the admin to enter the volunteer's new username."""
    print("\nVolunteer's current username is:", username)
    logging.debug("Admin prompted to enter new username.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_username = input("Enter new username: ").strip()
        if new_username == "0":
            logging.debug("Returning to previous step.")
            return
        if new_username == username:
            print("New username is the same as current username. Please enter a different username.")
            logging.error("Username is unchanged.")
            continue
        if new_username == "":
            print("Please enter a username.")
            logging.error("Admin did not enter a username.")
            continue
        s = re.search("^[a-zA-Z]+[a-zA-Z0-9_]*$", new_username)
        if not s:
            print("Username can only contain letters, digits (0-9) and underscore (_), and must start with a letter. Please choose another username.")
            logging.error("Invalid user input.")
            continue
        users = pd.read_csv('users.csv', dtype={'password': str})
        select_username = users[users['username'] == new_username]
        if len(select_username.index) > 0:  # username already exists
            print("Username is taken. Please choose another username.")
            logging.error("Admin entered a username that already exists.")
            continue
        break
    # update csv file
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'username'] = new_username
    users = users.sort_values(by=['username'])  # sort by username before saving
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")

    # also update for volunteering sessions
    vol_times = pd.read_csv("volunteering_times.csv")
    vol_times.loc[vol_times["username"] == username, "username"] = new_username
    vol_times.to_csv('volunteering_times.csv', index=False)
    logging.debug("volunteering_times.csv updated")

    print("Volunteer's new username is:", new_username)
    logging.debug("Username updated successfully")
    return

def edit_password(username, password):
    """Prompts the admin to enter the volunteer's new password."""
    print("\n" + username + "'s current password is:", password)
    logging.debug("Admin prompted to enter new password.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_password = input("Enter new password: ")
        if new_password == "0":
            logging.debug("Returning to previous step.")
            return
        if new_password == password:
            print("New password is the same as current password. Please enter a different password.")
            logging.error("Password is unchanged.")
            continue
        if len(new_password) < 3:
            print("Password should be at least 3 characters.")
            logging.error("Invalid user input.")
            continue
        s = re.search("[, ]", new_password)
        if s:
            print("Password cannot contain commas or spaces. Please choose another password.")
            logging.error("Invalid user input.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'password'] = new_password
    users.to_csv('users.csv', index=False)
    print("You have changed " + username + "'s password to:", new_password)
    logging.debug("Password updated successfully")
    return

def edit_first_name(username, first_name):
    """Prompts the admin to enter the volunteer's new first name."""
    print("\n" + username + "'s current first name is:", first_name)
    logging.debug("Admin prompted to enter new first name.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_fname = input("Enter new first name: ").strip()
        if new_fname == "0":
            logging.debug("Returning to previous step.")
            return
        if new_fname == first_name:
            print("New first name is the same as current first name. Please enter a different first name.")
            logging.error("First name is unchanged.")
            continue
        if new_fname == "":
            print("Please enter a first name.")
            logging.error("Admin did not enter a first name.")
            continue
        s = re.search("^[A-Z][a-zA-Z-' ]*$", new_fname)
        if not s:
            print("First name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
            logging.error("Invalid user input.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'first_name'] = new_fname
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")
    print("You have changed " + username + "'s first name to:", new_fname)
    logging.debug("First name updated successfully")
    return

def edit_last_name(username, last_name):
    """Prompts the admin to enter the volunteer's new last name."""
    print("\n" + username + "'s current last name is:", last_name)
    logging.debug("Admin prompted to enter new last name.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_lname = input("Enter new last name: ").strip()
        if new_lname == "0":
            logging.debug("Returning to previous step.")
            return
        if new_lname == last_name:
            print("New last name is the same as current last name. Please enter a different last name.")
            logging.error("Last name is unchanged.")
            continue
        if new_lname == "":
            print("Please enter a last name.")
            logging.error("Admin did not enter a last name.")
            continue
        s = re.search("^[a-zA-Z-' ]+$", new_lname)
        if not s:
            print("Last name can only contain letters, hyphen (-) and apostrophe (').")
            logging.error("Invalid user input.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'last_name'] = new_lname
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")
    print("You have changed " + username + "'s last name to:", new_lname)
    logging.debug("Last name updated successfully")
    return

def edit_gender(username, gender):
    """Prompts the admin to select the volunteer's new gender."""
    gender_str = convert_gender(gender)
    print("\n" + username + "'s current gender is:", gender_str)
    logging.debug("Admin prompted to enter new gender.")
    while True:
        print("Enter [0] to return to the previous step.")
        print("New gender:")
        print("Enter [1] for male")
        print("Enter [2] for female")
        print("Enter [3] for non-binary")
        try:
            new_gender = int(input("Select an option: "))
            if new_gender not in range(4):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        if new_gender == 0:
            logging.debug("Returning to previous step.")
            return
        if new_gender == gender:
            print("New gender is the same as current gender. Please try again or return to the previous step.")
            logging.error("Gender is unchanged.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'gender'] = new_gender
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")

    new_gender_str = convert_gender(new_gender)
    print("You have changed " + username + "'s gender to:", new_gender_str)
    logging.debug("Gender updated successfully")
    return

def edit_dob(username, date_of_birth):
    """
    Prompts the admin to enter the volunteer's corrected date of birth.
    The volunteer must be aged 18-99.
    """
    print("\n" + username + "'s current date of birth (DD-MM-YYYY) is:", date_of_birth)
    logging.debug("Admin prompted to enter corrected date of birth.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_dob = input("Enter corrected date of birth: ").strip()
        if new_dob == "0":
            logging.debug("Returning to previous step.")
            return
        if new_dob == date_of_birth:
            print("New date of birth is the same as current date of birth. Please try again or return to the previous step.")
            logging.error("Date of birth is unchanged.")
            continue
        try:
            ndob = datetime.datetime.strptime(new_dob, "%d-%m-%Y").date()
        except ValueError:
            print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
            logging.error("Invalid user input.")
            continue
        t = datetime.date.today()
        if ndob > t:
            print("Date of birth cannot be in the future. Please try again.")
            logging.error("Admin entered a date of birth in the future.")
            continue
        if t.year - ndob.year < 18 or (t.year - ndob.year == 18 and t.month < ndob.month) or (
                t.year - ndob.year == 18 and t.month == ndob.month and t.day < ndob.day):
            print("Volunteers must be at least 18 years old.")
            logging.error("Volunteer is less than 18 years old based on date of birth.")
            continue
        if t.year - ndob.year > 100 or (t.year - ndob.year == 100 and t.month > ndob.month) or (
                t.year - ndob.year == 100 and t.month == ndob.month and t.day >= ndob.day):
            print("Volunteers must be 18-99 years old (inclusive).")
            logging.error("Volunteer is more than 99 years old based on date of birth.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'date_of_birth'] = new_dob
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")
    print("You have corrected " + username + "'s date of birth to:", new_dob)
    logging.debug("Date of birth updated successfully")
    return

def edit_email(username, email):
    """Prompts the admin to enter the volunteer's new email address."""
    print("\n" + username + "'s current email address is:", email)
    logging.debug("Admin prompted to enter new email address.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_email = input("Enter new email address: ").strip()
        if new_email == "0":
            logging.debug("Returning to previous step.")
            return
        if new_email == email:
            print("New email is the same as current email. Please enter a different email address.")
            logging.error("Email address is unchanged.")
            continue
        if new_email == "":
            print("Please enter an email address.")
            logging.error("Admin did not enter an email address.")
            continue
        s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", new_email)
        if not s:
            print("Invalid email address. Please try again.")
            logging.error("Invalid user input.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'email'] = new_email
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")
    print("You have changed " + username + "'s email address to:", new_email)
    logging.debug("Email address updated successfully")
    return

def edit_phone_num(username, phone_number):
    """Prompts the admin to enter the volunteer's new phone number."""
    print("\n" + username + "'s current phone number is:", phone_number)
    logging.debug("Admin prompted to enter new phone number.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_phone_num = input("Enter new phone number: ").strip()
        if new_phone_num == "0":
            logging.debug("Returning to previous step.")
            return
        if new_phone_num == phone_number:
            print("New phone number is the same as current phone number. Please enter a different phone number.")
            logging.error("Phone number is unchanged.")
            continue
        if new_phone_num == "":
            print("Please enter a phone number.")
            logging.error("Admin did not enter a phone number.")
            continue
        s = re.search("^\+?\d{1,3} \d{8,11}$", new_phone_num)  # allow starting + to be omitted
        if not s:
            print("Incorrect phone number format. Please try again.")
            logging.error("Invalid user input.")
            continue
        if new_phone_num[0] != "+":
            new_phone_num = "+" + new_phone_num
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'phone_number'] = new_phone_num
    users.to_csv('users.csv', index=False)
    logging.debug("users.csv updated")
    print("You have changed " + username + "'s phone number to:", new_phone_num)
    logging.debug("Phone number updated successfully")
    return
