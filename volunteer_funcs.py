import pandas as pd, re, datetime
from coded_vars import convert_gender

def add_plan():
    plans = pd.read_csv('humanitarian_plan.csv')
    plans = plans[plans['end_date'].isna()]  # only show plans that haven't been closed

    if len(plans.index) == 0:
        print("\nThere are no ongoing humanitarian plans. Please check back later.")
        return "X"

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
            print("Please enter a number from the options provided.\n")
            continue
        break

    plan_id = plans['plan_id'].iloc[plan_num - 1]
    print("Your plan ID is:", plan_id)
    return plan_id  # e.g. London_2023


def add_camp(plan_id):
    camps = pd.read_csv(plan_id + '.csv')

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
            continue

        camp_name = "Camp " + str(camp_num)
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
            print("Please enter a number from the options provided.")
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

##############################################
# Functions for admin to edit volunteer details
def edit_username(username):
    print("\nVolunteer's current username is:", username)
    while True:
        print("Enter [0] to return to the previous step.")
        new_username = input("Enter new username: ").strip()
        if new_username == "0":
            return
        if new_username == username:
            print("New username is the same as current username. Please enter a different username.")
            continue
        if new_username == "":
            print("Please enter a username.")
            continue
        s = re.search("^[a-zA-Z]+[a-zA-Z0-9_]*$", new_username)
        if not s:
            print("Username can only contain letters, digits (0-9) and underscore (_), and must start with a letter. Please choose another username.")
            continue
        users = pd.read_csv('users.csv', dtype={'password': str})
        select_username = users[users['username'] == new_username]
        if len(select_username.index) > 0:  # username already exists
            print("Username is taken. Please choose another username.")
            continue
        break
    # update csv file
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'username'] = new_username
    users = users.sort_values(by=['username'])  # sort by username before saving
    users.to_csv('users.csv', index=False)

    # also update for volunteering sessions
    vol_times = pd.read_csv("volunteering_times.csv")
    vol_times.loc[vol_times["username"] == username, "username"] = new_username
    vol_times.to_csv('volunteering_times.csv', index=False)

    print("Volunteer's new username is:", new_username)
    return

def edit_password(username, password):
    print("\n" + username + "'s current password is:", password)
    while True:
        print("Enter [0] to return to the previous step.")
        new_password = input("Enter new password: ")
        if new_password == "0":
            return
        if new_password == password:
            print("New password is the same as current password. Please enter a different password.")
            continue
        if len(new_password) < 3:
            print("Password should be at least 3 characters.")
            continue
        s = re.search("[, ]", new_password)
        if s:
            print("Password cannot contain commas or spaces. Please choose another password.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'password'] = new_password
    users.to_csv('users.csv', index=False)
    print("You have changed " + username + "'s password to:", new_password)
    return

def edit_first_name(username, first_name):
    print("\n" + username + "'s current first name is:", first_name)
    while True:
        print("Enter [0] to return to the previous step.")
        new_fname = input("Enter new first name: ").strip()
        if new_fname == "0":
            return
        if new_fname == first_name:
            print("New first name is the same as current first name. Please enter a different first name.")
            continue
        if new_fname == "":
            print("Please enter a first name.")
            continue
        s = re.search("^[A-Z][a-zA-Z-' ]*$", new_fname)
        if not s:
            print("First name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'first_name'] = new_fname
    users.to_csv('users.csv', index=False)
    print("You have changed " + username + "'s first name to:", new_fname)
    return

def edit_last_name(username, last_name):
    print("\n" + username + "'s current last name is:", last_name)
    while True:
        print("Enter [0] to return to the previous step.")
        new_lname = input("Enter new last name: ").strip()
        if new_lname == "0":
            return
        if new_lname == last_name:
            print("New last name is the same as current last name. Please enter a different last name.")
            continue
        if new_lname == "":
            print("Please enter a last name.")
            continue
        s = re.search("^[a-zA-Z-' ]+$", new_lname)
        if not s:
            print("Last name can only contain letters, hyphen (-) and apostrophe (').")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'last_name'] = new_lname
    users.to_csv('users.csv', index=False)
    print("You have changed " + username + "'s last name to:", new_lname)
    return

def edit_gender(username, gender):
    gender_str = convert_gender(gender)

    print("\n" + username + "'s current gender is:", gender_str)
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
            continue
        if new_gender == 0:
            return
        if new_gender == gender:
            print("New gender is the same as current gender. Please try again or return to the previous step.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'gender'] = new_gender
    users.to_csv('users.csv', index=False)

    new_gender_str = convert_gender(new_gender)
    print("You have changed " + username + "'s gender to:", new_gender_str)
    return

def edit_dob(username, date_of_birth):
    print("\n" + username + "'s current date of birth (DD-MM-YYYY) is:", date_of_birth)
    while True:
        print("Enter [0] to return to the previous step.")
        new_dob = input("Enter corrected date of birth: ").strip()
        if new_dob == "0":
            return
        if new_dob == date_of_birth:
            print("New date of birth is the same as current date of birth. Please try again or return to the previous step.")
            continue
        try:
            ndob = datetime.datetime.strptime(new_dob, "%d-%m-%Y").date()
        except ValueError:
            print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
            continue
        t = datetime.date.today()
        if ndob > t:
            print("Date of birth cannot be in the future. Please try again.")
            continue
        if t.year - ndob.year < 18 or (t.year - ndob.year == 18 and t.month < ndob.month) or (
                t.year - ndob.year == 18 and t.month == ndob.month and t.day < ndob.day):
            print("Volunteers must be at least 18 years old.")
            continue
        if t.year - ndob.year > 100 or (t.year - ndob.year == 100 and t.month > ndob.month) or (
                t.year - ndob.year == 100 and t.month == ndob.month and t.day >= ndob.day):
            print("Volunteers must be 18-99 years old (inclusive).")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'date_of_birth'] = new_dob
    users.to_csv('users.csv', index=False)
    print("You have corrected " + username + "'s date of birth to:", new_dob)
    return

def edit_email(username, email):
    print("\n" + username + "'s current email address is:", email)
    while True:
        print("Enter [0] to return to the previous step.")
        new_email = input("Enter new email address: ").strip()
        if new_email == "0":
            return
        if new_email == email:
            print("New email is the same as current email. Please enter a different email address.")
            continue
        if new_email == "":
            print("Please enter an email address.")
            continue
        s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", new_email)
        if not s:
            print("Invalid email address. Please try again.")
            continue
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'email'] = new_email
    users.to_csv('users.csv', index=False)
    print("You have changed " + username + "'s email address to:", new_email)
    return

def edit_phone_num(username, phone_number):
    print("\n" + username + "'s current phone number is:", phone_number)
    while True:
        print("Enter [0] to return to the previous step.")
        new_phone_num = input("Enter new phone number: ").strip()
        if new_phone_num == "0":
            return
        if new_phone_num == phone_number:
            print("New phone number is the same as current phone number. Please enter a different phone number.")
            continue
        if new_phone_num == "":
            print("Please enter a phone number.")
            continue
        s = re.search("^\+?\d{1,3} \d{8,11}$", new_phone_num)  # allow starting + to be omitted
        if not s:
            print("Incorrect phone number format. Please try again.")
            continue
        if new_phone_num[0] != "+":
            new_phone_num = "+" + new_phone_num
        break
    # update csv file
    users = pd.read_csv('users.csv', dtype={'password': str})
    cur_user = (users['username'] == username)
    users.loc[cur_user, 'phone_number'] = new_phone_num
    users.to_csv('users.csv', index=False)
    print("You have changed " + username + "'s phone number to:", new_phone_num)
    return