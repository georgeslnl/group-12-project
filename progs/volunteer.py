# built-in modules
import pandas as pd, numpy as np, re, datetime, os
import logging
# custom modules and functions from other files
from progs.coded_vars import convert_gender, convert_medical_condition
from progs import refugee_profile_funcs, volunteering_session_funcs, resource_consumption
from progs import verify as v

class Volunteer:
    """Class for Volunteer users. Initialised when a user successfully logs in as a volunteer."""
    def __init__(self, username, password, first_name, last_name, email, phone_number, gender, date_of_birth, plan_id, camp_name):
        """Initialises attributes with the user's details."""
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.plan_id = plan_id
        self.camp_name = camp_name
        self.logged_in = True

    def volunteer_menu(self):
        """Main menu when a volunteer logs in, providing options to access sub-menus and methods for the various volunteer functionalities."""
        while self.logged_in:
            logging.debug(f"{self.username} has entered the volunteer menu.")
            print("\n--------------------------------------------")
            print("\t\tVOLUNTEER MENU")
            print("Welcome,", self.first_name, self.last_name)
            if self.camp_name is None:
                print("\n* You are not currently assigned to a camp. Please update your camp identification. *")
                logging.info(f"{self.username} is not assigned to a camp. A notification has been displayed.")
            while True:
                print("\nWhat would you like to do?")
                print("Enter [1] for personal information and camp identification")
                print("Enter [2] to create, view, edit or remove a refugee profile")
                print("Enter [3] to display or update your camp's information (including resource requests)")
                print("Enter [4] to request account deactivation")
                print("Enter [5] to add, view or remove volunteering sessions")
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
                logging.info(f'{self.username} has logged out of their session.')
                self.logout()
            if option == 1:
                logging.debug(f"{self.username} has selected the personal information menu.")
                self.personal_menu()
            if option == 2:
                logging.debug(f"{self.username} has selected the refugee profile menu.")
                self.refugee_menu()
            if option == 3:
                logging.debug(f"{self.username} has selected the camp information menu.")
                self.camp_info_menu()
            if option == 4:
                logging.debug(f"{self.username} has selected to request account deactivation.")
                self.request_deactivation()
            if option == 5:
                logging.debug(f"{self.username} has selected the volunteering session menu.")
                self.volunteering_session_menu()

    def personal_menu(self):
        """Sub-menu enabling the volunteer to access functionalities relating to their personal information and camp identification."""
        while True:
            logging.debug(f"{self.username} has entered the personal information menu.")
            print("\n--------------------------------------------")
            print(" PERSONAL INFORMATION & CAMP IDENTIFICATION")
            while True:
                print("Enter [1] to view your personal information")
                print("Enter [2] to edit your personal information")
                print("Enter [3] to update your camp identification")
                print("Enter [0] to return to the volunteer menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(4):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f"{self.username} has chosen to return to the volunteer menu.")
                return
            if option == 1:
                logging.debug(f"{self.username} has chosen to view their personal information.")
                self.view_personal_info()
            if option == 2:
                logging.debug(f"{self.username} has chosen to edit their personal information.")
                self.edit_personal_info()
            if option == 3:
                logging.debug(f"{self.username} has chosen to update their camp identification.")
                self.update_camp()

    def refugee_menu(self):
        """Sub-menu enabling the volunteer to access functionalities relating to refugee profiles.
        Volunteers must have a camp to access the menu."""
        while True:
            logging.debug(f"{self.username} has entered the refugee profile menu.")
            print("\n--------------------------------------------")
            print("\tMANAGE REFUGEE PROFILES")
            if not self.camp_name:
                logging.debug(f"{self.username} does not have a camp on their profile.")
                print("\nVolunteers can only manage refugee profiles for their current camp. "
                      "\nYou are currently not assigned to a camp."
                      "\nPlease add your camp identification.")
                return

            while True:
                print("Enter [1] to create a new refugee profile")
                print("Enter [2] to view a refugee profile")
                print("Enter [3] to edit or remove a refugee profile")
                print("Enter [0] to return to the volunteer menu\n")
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
                logging.debug(f"{self.username} has chosen to return to the volunteer menu.")
                return
            if option == 1:
                logging.debug(f'{self.username} has chosen to create a refugee profile.')
                self.create_refugee_profile()
            if option == 2:
                logging.debug(f'{self.username} has chosen to view a refugee profile.')
                self.view_refugee_profile()
            if option == 3:
                logging.debug(f'{self.username} has chosen to edit or remove a refugee profile.')
                self.edit_refugee_profile()

    def camp_info_menu(self):
        """
        Sub-menu enabling the volunteer to access functionalities relating to their current camp's information (capacity and resources).
        Volunteers must have a camp to access the menu.
        """
        while True:
            logging.debug(f"{self.username} has entered the camp information menu.")
            print("\n--------------------------------------------")
            print("\t\tCAMP INFORMATION")
            if not self.camp_name:
                print("\nYou are currently not assigned to a camp."
                      "\nPlease add your camp identification in order to display or update camp information.")
                return

            while True:
                print("Enter [1] to display your camp's information")
                print("Enter [2] to update your camp's information")
                print("Enter [3] to request resources for your camp")
                print("Enter [0] to return to the volunteer menu\n")
                try:
                    option = int(input(">>Enter you option: "))
                    if option not in range(4):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f'{self.username} has chosen to return to the volunteer menu.')
                return
            if option == 1:
                logging.debug(f'{self.username} has chosen to display camp information.')
                self.display_camp_info()
            if option == 2:
                logging.debug(f'{self.username} has chosen to update camp information.')
                self.update_camp_info()
            if option == 3:
                logging.debug(f'{self.username} has chosen to request resources.')
                self.request_resources()

    def volunteering_session_menu(self):
        """
        Sub-menu enabling the volunteer to access functionalities relating to volunteering sessions.
        Volunteers must have a camp to access the menu.
        """
        while True:
            logging.debug(f"{self.username} has entered the volunteering sessions menu.")
            print("\n--------------------------------------------")
            print("\tMANAGE VOLUNTEERING SESSIONS")
            print("Tell us when you are coming to volunteer.")
            if not self.camp_name:
                print("\nYou are currently not assigned to a camp."
                      "\nPlease add your camp identification in order to manage volunteering sessions.")
                return

            while True:
                print("Enter [1] to add a volunteering session")
                print("Enter [2] to view your volunteering sessions")
                print("Enter [3] to remove a volunteering session")
                print("Enter [0] to return to the volunteer menu\n")
                try:
                    user_input = input(">>Select an option: ")
                    option = int(user_input)
                    if option not in range(4):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            if option == 0:
                logging.debug(f'{self.username} has chosen to return to the volunteer menu.')
                return
            if option == 1:
                logging.debug(f'{self.username} has chosen to add a volunteering session.')
                self.add_volunteering_session()
            if option == 2:
                logging.debug(f'{self.username} has chosen to view their volunteering sessions.')
                self.view_volunteering_sessions()
            if option == 3:
                logging.debug(f'{self.username} has chosen to remove a volunteering session.')
                self.remove_volunteering_session()

    def logout(self):
        """Changes the user's logged_in attribute to False, causing the user to log out."""
        self.logged_in = False
        print("You are now logged out. See you again!\n")

    def request_deactivation(self):
        """
        Enables the volunteer to request for their account to be deactivated.
        The admin will subsequently be notified of the request.
        """
        print("\n--------------------------------------------")
        print("\tREQUEST ACCOUNT DEACTIVATION")
        logging.debug(f'{self.username} prompted to confirm deactivation request.')
        while True:
            print("Are you sure you would like to deactivate your account?")
            print("If your request is approved, you will no longer be able to "
                  "volunteer at any humanitarian plans or login to the system.")
            print("To reactivate your account subsequently, you will need to contact an administrator.")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the volunteer menu\n")
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.\n")
                logging.error("Invalid user input.")
                continue
            break
        if option == 0:
            logging.debug("Returning to the volunteer menu.")
            return

        logging.debug("Deactivation request confirmed.")
        # update csv files
        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        cur_user = (users['username'] == self.username)
        users.loc[cur_user, 'deactivation_requested'] = 1
        users.to_csv(os.path.join('data', 'users.csv'), index=False)
        logging.info("users.csv updated")

        print("\nYour request to deactivate your account has been registered.")
        print("An administrator will respond to your request shortly.")
        return

    def view_personal_info(self):
        """
        Enables the volunteer to view their personal information (excludes camp identification).
        An additional option is presented for the volunteer to select whether to display their password.
        """
        gender_str = convert_gender(self.gender)

        print("\n--------------------------------------------")
        print("\tVIEW PERSONAL INFORMATION")
        print("Your details are as follows:")
        print("Username:", self.username)
        print("First name:", self.first_name)
        print("Last name:", self.last_name)
        print("Email:", self.email)
        print("Phone number:", self.phone_number)
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", self.date_of_birth)

        logging.debug(f"{self.username}'s personal information has been displayed.")
        logging.debug(f'{self.username} prompted whether to view their password.')

        while True:
            print("\nEnter [1] if you would like to view your password. The password will appear in plain text.")
            print("Enter [0] to return to the previous menu")
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break
        if option == 1:
            logging.debug(f"{self.username} has chosen to view their password.")
            print("\nYour password is:", self.password)
        else:
            logging.debug(f"{self.username} has chosen not to view their password.")
        return

    def edit_personal_info(self):
        """
        Enables the volunteer to edit their personal details (excluding date of birth).
        A menu enables the volunteer to edit multiple details before leaving the method.
        """
        def edit_username():
            """Prompts the volunteer to enter their new username."""
            print("\nYour current username is:", self.username)
            logging.debug(f"{self.username} prompted to enter new username.")
            while True:
                print("Enter [0] to return to the previous step.\n")
                new_username = v.username(">>Enter new username: ").strip()
                if new_username == "0":
                    logging.debug("Returning to previous step.")
                    return
                if new_username == self.username:
                    print("\nNew username is the same as current username.\n")
                    logging.error("Invalid user input.")
                    continue
                users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
                select_username = users[users['username'] == new_username]
                if len(select_username.index) > 0:  # username already exists
                    print('\nUsername "' + new_username + '"is taken. '
                                                          '\nPlease choose another username.\n')
                    logging.error(f"{self.username} entered a username that already exists.")
                    continue
                break
            # update csv file
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'username'] = new_username
            users = users.sort_values(by=['username'])  # sort by username before saving
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")

            # also update for volunteering sessions
            vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
            vol_times.loc[vol_times["username"] == self.username, "username"] = new_username
            vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
            logging.debug("volunteering_times.csv updated")
            print("\nUsername updated successfully!")
            print("Your new username is:", new_username)
            self.username = new_username
            logging.debug("Username updated successfully")
            return

        def edit_password():
            """Prompts the volunteer to enter their new password."""
            print("\nYour current password is:", self.password)
            while True:
                print("Enter [0] to return to the previous step.\n")
                new_password = input(">>Enter new password: ")
                if new_password == "0":
                    logging.debug("Returning to previous step.")
                    return
                if new_password == self.password:
                    print("\nNew password is the same as current password. "
                          "\nPlease enter a different password.\n")
                    logging.error("Password is unchanged.")
                    continue
                if len(new_password) < 3:
                    print("\nPassword should be at least 3 characters.\n")
                    logging.error("Invalid user input.")
                    continue
                s = re.search("[, ]", new_password)
                if s:
                    print("\nPassword cannot contain commas or spaces. "
                          "\nPlease choose another password.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            # update csv file
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'password'] = new_password
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print("\nPassword updated successfully!")
            print("Your new password is:", new_password)
            self.password = new_password
            logging.debug("Password updated successfully")
            return

        def edit_first_name():
            """Prompts the volunteer to enter their new first name."""
            print("\nYour current first name is:", self.first_name)
            logging.debug(f"{self.username} prompted to enter new first name.")
            while True:
                print("Enter [0] to return to the previous step.\n")
                new_fname = v.name(">>Enter new first name: ").strip()
                if new_fname == "0":
                    logging.debug("Returning to previous step.")
                    return
                elif new_fname == self.first_name:
                    print("New first name is the same as current first name. ")
                else:
                    # Capitalise the first letter instead of requiring input again
                    new_fname = f"{new_fname[0].upper()}{new_fname[1:]}"
                    break
            # update csv file
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'first_name'] = new_fname
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print("\nFirst name updated successfully!")
            print("You have changed your first name to:", new_fname)
            self.first_name = new_fname
            logging.debug("First name updated successfully")
            return

        def edit_last_name():
            """Prompts the volunteer to enter their new last name."""
            print("\nYour current last name is:", self.last_name)
            logging.debug(f"{self.username} prompted to enter new last name.")
            while True:
                print("Enter [0] to return to the previous step.\n")
                new_lname = v.name(">>Enter new last name: ").strip()
                if new_lname == "0":
                    logging.debug("Returning to previous step.")
                    return
                elif new_lname == self.last_name:
                    print("New last name is the same as current last name.")
                else:
                    break
            # update csv file
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'last_name'] = new_lname
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print("\nLast name updated successfully!")
            print("You have changed your last name to:", new_lname)
            self.last_name = new_lname
            logging.debug("Last name updated successfully")
            return

        def edit_gender():
            """Prompts the volunteer to select their new gender."""
            gender_str = convert_gender(self.gender)
            print("\nYour current gender is:", gender_str)
            logging.debug(f"{self.username} prompted to select new gender.")
            while True:
                print("Enter [0] to return to the previous step.")
                print("New gender:")
                print("Enter [1] for male")
                print("Enter [2] for female")
                print("Enter [3] for non-binary\n")
                try:
                    new_gender = int(input(">>Select an option: "))
                    if new_gender not in range(4):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue
                if new_gender == 0:
                    logging.debug("Returning to previous step.")
                    return
                if new_gender == self.gender:
                    print("\nYour selection is the same as current gender."
                          "\nPlease try again or return to the previous step.\n")
                    logging.error("Gender is unchanged.")
                    continue
                break
            # update csv file
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'gender'] = new_gender
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")

            new_gender_str = convert_gender(new_gender)
            print("\nGender updated successfully!")
            print("You have changed your gender to:", new_gender_str)
            self.gender = new_gender
            logging.debug("Gender updated successfully")
            return

        def edit_email():
            """Prompts the volunteer to enter their new email address."""
            print("\nYour current email address is:", self.email)
            logging.debug(f"{self.username} prompted to enter new email address.")
            while True:
                print("Enter [0] to return to the previous step.\n")
                new_email = input(">>Enter new email address: ").strip()
                if new_email == "0":
                    logging.debug("Returning to previous step.")
                    return
                if new_email == self.email:
                    print("\nNew email is the same as current email.\n")
                    logging.error("Email address is unchanged.")
                    continue
                if new_email == "":
                    print("\nPlease enter an email address.\n")
                    logging.error(f"{self.username} did not enter an email address.")
                    continue
                s = re.search("^[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z.]+$", new_email)
                if not s:
                    print("\nInvalid email address. Please try again.\n")
                    logging.error("Invalid user input.")
                    continue
                break
            # update csv file
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'email'] = new_email
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print("\nEmail address updated successfully!")
            print("You have changed your email address to:", new_email)
            self.email = new_email
            logging.debug("Email address updated successfully")
            return

        def edit_phone_num():
            """Prompts the volunteer to enter their new phone number."""
            print("\nYour current phone number is:", self.phone_number)
            logging.debug(f"{self.username} prompted to enter new phone number.")
            while True:
                print("Enter [0] to return to the previous step.\n")
                new_phone_num = input(">>Enter new phone number: ").strip()
                if new_phone_num == "0":
                    logging.debug("Returning to previous step.")
                    return
                if new_phone_num == self.phone_number:
                    print("\nNew phone number is the same as current phone number.")
                    logging.error("Phone number is unchanged.")
                    continue
                if new_phone_num == "":
                    print("\nPlease enter a phone number.\n")
                    logging.error(f"{self.username} did not enter a phone number.")
                    continue
                s = re.search("^\+?\d{1,3} \d{8,11}$", new_phone_num)  # allow starting + to be omitted
                if not s:
                    print("\nIncorrect phone number format. Please try again.\n")
                    logging.error("Invalid user input.")
                    continue
                if new_phone_num[0] != "+":
                    new_phone_num = "+" + new_phone_num
                break
            # update csv file
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'phone_number'] = new_phone_num
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")
            print("\nPhone number updated successfully!")
            print("You have changed your phone number to:", new_phone_num)
            self.phone_number = new_phone_num
            logging.debug("Phone number updated successfully")
            return

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            print("\n--------------------------------------------")
            print("\tEDIT PERSONAL INFORMATION")
            # inner loop to catch invalid input
            while True:
                logging.debug(f"{self.username} prompted to select which detail to edit.")
                print("Which details would you like to update?")
                print("Enter [1] for username")
                print("Enter [2] for password")
                print("Enter [3] for first name")
                print("Enter [4] for last name")
                print("Enter [5] for gender")
                print("Enter [6] for email")
                print("Enter [7] for phone number")
                print("Enter [0] to return to the previous menu\n")
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
                logging.debug(f"{self.username} has finished editing their personal details. Returning to personal information menu.")
                return
            if option == 1:
                edit_username()
            if option == 2:
                edit_password()
            if option == 3:
                edit_first_name()
            if option == 4:
                edit_last_name()
            if option == 5:
                edit_gender()
            if option == 6:
                edit_email()
            if option == 7:
                edit_phone_num()


    def update_camp(self):
        """
        Enables the volunteer to update their camp identification.
        If the volunteer currently does not have a camp, they are prompted to select a camp.
        If the volunteer currently has a camp, they can select whether to change the camp or remove their camp identification.
        """
        def add_camp(plan_id):
            """Prompts the volunteer to select a camp if they currently do not have a camp."""
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            logging.debug(f"{self.username} currently has no camp and is prompted to select a camp.")
            while True:
                print("\nPlease choose a camp from the list below.")
                print("Camp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                print("Enter [X] to return to the previous menu.\n")
                camp_num = input(">>Enter the number corresponding to the camp you would like to join "
                                 "(e.g. [1] for Camp 1): ")
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
                logging.debug(f"{self.username} has joined {new_camp}.")
                return new_camp

        def edit_camp(plan_id):
            """Prompts the volunteer to select a new camp if they currently have a camp."""
            camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
            if len(camps.index) == 1:
                print("There is currently only one camp in your plan. "
                      "\nUnable to change your camp identification now.")
                logging.warning(f"There is only one camp at {self.plan_id}. Not possible to change camps.")
                return self.camp_name

            logging.debug(f"{self.username} prompted to select new camp.")
            while True:
                print("\nPlease choose a new camp from the list below.")
                print("Camp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                print("Enter [X] to return to the previous menu.\n")
                camp_num = input(">>Enter the number corresponding to the camp you would like to join "
                                 "(e.g. [1] for Camp 1): ")
                if camp_num.upper() == "X":
                    logging.debug("Returning to previous menu without making changes.")
                    return self.camp_name
                try:
                    camp_num = int(camp_num)
                    if camp_num not in range(1, len(camps.index) + 1):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter the number of a camp from the list displayed.")
                    logging.error("Invalid user input.")
                    continue
                new_camp = "Camp " + str(camp_num)
                if new_camp == self.camp_name:
                    print("\nNew camp is the same as current camp. "
                          "\nPlease try again or return to the previous menu.")
                    logging.error("Camp is unchanged.")
                    continue
                logging.debug(f"{self.username} has changed to {new_camp}.")
                return new_camp

        print("\n--------------------------------------------")
        print("\tUPDATE CAMP IDENTIFICATION")
        print("You are volunteering at plan ID:", self.plan_id)
        print("Your current camp is:", self.camp_name)
        if not self.camp_name:
            new_camp = add_camp(self.plan_id)
        else:
            logging.debug(f"{self.username} prompted to choose between updating and removing camp identification.")
            while True:
                print("Enter [1] to update camp identification")
                print("Enter [2] to remove camp identification")
                print("Enter [0] to return to the previous menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(3):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.\n")
                    logging.error("Invalid user input.")
                    continue

                if option == 0:
                    logging.debug("Returning to previous menu.")
                    return
                if option == 1:
                    new_camp = edit_camp(self.plan_id)
                if option == 2:
                    logging.debug(f"{self.username} prompted to confirm removal of camp identification.")
                    while True:
                        print("\nAre you sure you would like to remove your camp identification and leave this camp?")
                        print("All your volunteering sessions at this camp will be erased.")
                        print("Enter [1] to proceed")
                        print("Enter [0] to go back to the previous step\n")
                        try:
                            remove_option = int(input(">>Select an option: "))
                            if remove_option not in (0, 1):
                                raise ValueError
                        except ValueError:
                            print("\nPlease enter a number from the options provided.\n")
                            logging.error("Invalid user input.")
                            continue
                        break
                    if remove_option == 0:
                        logging.debug("Returning to previous step.")
                        continue
                    new_camp = None
                    logging.debug(f"{self.username}'s camp identification has been removed.")
                break

        # update csv files
        if new_camp != self.camp_name:
            users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'camp_name'] = new_camp
            users.to_csv(os.path.join('data', 'users.csv'), index=False)
            logging.debug("users.csv updated")

            camps = pd.read_csv(os.path.join('data', self.plan_id + '.csv'))
            if new_camp:
                chosen = (camps['camp_name'] == new_camp)
                camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            if self.camp_name:
                old = (camps['camp_name'] == self.camp_name)
                camps.loc[old, 'volunteers'] = camps.loc[old, 'volunteers'] - 1
            camps.to_csv(os.path.join('data', self.plan_id + '.csv'), index=False)
            logging.debug("camps csv file updated")

            if self.camp_name and not new_camp: # remove volunteering sessions
                vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
                vol_times = vol_times.drop(vol_times[vol_times['username'] == self.username].index)
                vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
                logging.debug("volunteering_times.csv updated")
            if self.camp_name and new_camp: # change camp_name in volunteering_times.csv
                vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
                vol_times.loc[vol_times["username"] == self.username, "camp_name"] = new_camp
                vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
                logging.debug("volunteering_times.csv updated")

            print("\nCamp identification updated successfully!")
            print("Your new camp is:", new_camp)
            self.camp_name = new_camp
        return

    def create_refugee_profile(self):
        """
        Enables the volunteer to create a refugee profile at their current camp.
        The volunteer is prompted for the refugee's details one by one.
        """
        def add_name():
            """Prompts the user to input the refugee's name."""
            logging.debug("User prompted to enter refugee name.")
            while True:
                print("Enter [0] to return to the previous menu.\n")
                refugee_name = input(">>Enter refugee's name: ").strip()
                if refugee_name == "0":
                    return refugee_name
                # validation
                if refugee_name == "":
                    print("\nPlease enter a refugee name.\n")
                    logging.error("User did not enter a name.")
                    continue
                s = re.search("^[A-Z][a-zA-Z-' ]*$", refugee_name)
                if not s:
                    print("\nName can only contain letters, hyphen (-) and apostrophe ('), "
                          "and must start with a capital letter.\n")
                    logging.error("Invalid user input.")
                    continue
                return refugee_name

        print("\n--------------------------------------------")
        print("\tCREATE REFUGEE PROFILE")
        camps = pd.read_csv(os.path.join('data', self.plan_id + '.csv'))
        cur_camp = camps[camps['camp_name'] == self.camp_name]
        remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']

        if remaining_cap == 0:
            print("Your camp has reached its maximum capacity. Unable to add new refugees.")
            logging.warning(f"{self.username}'s camp is full. Returning to previous menu.")
            return
        print("Your camp's remaining capacity is " + str(remaining_cap) + ".")
        print("Please return to the previous menu if the refugee's family is larger than this number.")

        progress = 0
        # loop allowing user to go back
        while progress < 6:
            if progress == 0:
                refugee_name = add_name()
                if refugee_name == "0":
                    logging.debug("Returning to previous menu.")
                    return
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

        logging.debug(f"{self.username} has finished entering refugee details.")
        # Update csv tables
        refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
        if len(refugees.index) == 0:
            refugee_id = 1
        else:
            refugee_id = refugees['refugee_id'].iloc[-1] + 1
        new_row = {'refugee_id': [refugee_id], 'refugee_name': [refugee_name], 'gender': [gender],
                   'date_of_birth': [date_of_birth], 'plan_id': [self.plan_id], 'camp_name': [self.camp_name],
                   'medical_condition': [medical_cond], 'family_members': [family], 'remarks': [remarks]}
        new = pd.DataFrame(new_row)
        refugees = pd.concat([refugees, new], ignore_index=True)
        refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
        logging.debug("refugees.csv updated")

        camps = pd.read_csv(os.path.join('data', self.plan_id + '.csv'))
        chosen = (camps['camp_name'] == self.camp_name)
        camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] + family
        camps.to_csv(os.path.join('data', self.plan_id + '.csv'), index=False)
        logging.debug("camps csv file updated")

        # Print details provided
        gender_str = convert_gender(gender)
        medical_str = convert_medical_condition(medical_cond)

        print("\nNew refugee profile is created successfully!")
        print("Refugee ID: ", refugee_id)
        print("Refugee name:", refugee_name)
        print("Gender:", gender_str)
        print("Date of birth:", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        print("The refugee and their family have been added to " + self.camp_name + ".")
        return

    def view_refugee_profile(self):
        """Enables the volunteer to view the profile of a selected refugee at their camp."""
        print("\n--------------------------------------------")
        print("\tVIEW REFUGEE PROFILE")
        refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
        refugees = refugees[(refugees['plan_id'] == self.plan_id) & (refugees['camp_name'] == self.camp_name)]
        if len(refugees.index) == 0:
            print("There are no refugees at your current camp.")
            logging.warning(f"No refugees at {self.username}'s camp. Returning to previous menu.")
            return

        refugees = refugees.replace({np.nan: None})
        logging.debug(f"{self.username} prompted to select a refugee.")
        while True:
            print("Enter [1] to enter the refugee ID you would like to view")
            print("Enter [2] to list all refugees at your current camp")
            print("Enter [0] to return to the previous menu\n")
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.\n")
                logging.error("Invalid user input.")
                continue
            break
        if option == 0:
            logging.debug("Returning to previous menu.")
            return
        if option == 2: # list refugees at volunteer's camp
            logging.debug(f"{self.username} has chosen to list all refugees at their camp.")
            print("\nRefugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")

        # Obtain refugee ID
        while True:
            print("\nEnter [0] to return to the previous menu.\n")
            try:
                refugee_id = int(input(">>Enter refugee ID you would like to view: "))
                if refugee_id == 0:
                    logging.debug("Returning to previous menu.")
                    return
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("\nPlease enter a refugee ID corresponding to a refugee in your camp.")
                logging.error("Invalid user input.")
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

        logging.debug("Printing details of selected refugee.")
        print("\nDetails of refugee ID:", refugee_id)
        print("Camp name:", self.camp_name)
        print("Refugee name:", refugee_name)
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        return

    def edit_refugee_profile(self):
        """
        Enables the volunteer to edit the profile of a selected refugee at their camp.
        Once a refugee is selected, a menu enables the volunteer to edit multiple details before leaving the method.
        This includes an option to remove the refugee's profile.
        """
        print("\n--------------------------------------------")
        print("    EDIT OR REMOVE REFUGEE PROFILE")
        refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
        refugees = refugees[(refugees['plan_id'] == self.plan_id) & (refugees['camp_name'] == self.camp_name)]
        if len(refugees.index) == 0:
            print("There are no refugees at your current camp.")
            logging.warning(f"No refugees at {self.username}'s camp. Returning to previous menu.")
            return

        refugees = refugees.replace({np.nan: None})
        logging.debug(f"{self.username} prompted to select a refugee.")
        while True:
            print("Enter [1] to enter the refugee ID you would like to edit")
            print("Enter [2] to list all refugees at your current camp")
            print("Enter [0] to return to the previous menu\n")
            try:
                option = int(input(">>Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.\n")
                continue
            break
        if option == 0:
            logging.debug("Returning to previous menu.")
            return
        if option == 2: # list refugees at volunteer's camp
            print("\nRefugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")

        # Obtain refugee ID
        while True:
            print("\nEnter [0] to return to the previous menu.\n")
            try:
                refugee_id = int(input(">>Enter refugee ID you would like to edit: "))
                if refugee_id == 0:
                    logging.debug("Returning to previous menu.")
                    return
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("\nPlease enter a refugee ID corresponding to a refugee in your camp.\n")
                logging.error("Invalid user input.")
                continue
            break

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
                logging.debug(f"{self.username} prompted to select which detail to edit.")
                print("\nSelected refugee:", refugee_name)
                print("Which details would you like to update?")
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
                    if option not in (0,1,2,3,4,5,6,9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
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
                refugee_profile_funcs.edit_family(self.plan_id, self.camp_name, refugee_id, family)
            if option == 6:
                refugee_profile_funcs.edit_remarks(refugee_id, remarks)
            if option == 9:
                refugee_profile_funcs.remove_refugee(self.plan_id, self.camp_name, refugee_id, refugee_name, family)
                return

    def display_camp_info(self):
        """
        Enables the volunteer to view their camp's information.
        This includes number of volunteers and refugees, capacity, and resources available.
        """
        logging.debug(f"Printing details of {self.username}'s camp.")
        print("\n--------------------------------------------")
        print("\tDISPLAY CAMP INFORMATION")
        camps = pd.read_csv(os.path.join('data', self.plan_id + '.csv'))
        my_camp = camps[camps['camp_name'] == self.camp_name]
        print("Your camp is " + self.camp_name + " for plan ID " + self.plan_id + ".")
        print("Number of volunteers: ", my_camp.iloc[0]['volunteers'])
        print("Number of refugees: ", my_camp.iloc[0]['refugees'])
        print("Refugee capacity: ", my_camp.iloc[0]['capacity'])
        print("\nResources available")
        print("Food packets:", my_camp.iloc[0]['food'])
        print("Water portions:", my_camp.iloc[0]['water'])
        print("First-aid kits:", my_camp.iloc[0]['firstaid_kits'])
        return

    def update_camp_info(self):
        """
        Enables the volunteer to update their camp's capacity and record consumption of resources.
        A menu enables the volunteer to update multiple details before leaving the method.
        """
        def edit_capacity():
            """Prompts the volunteer to enter the new capacity of their camp."""
            camps = pd.read_csv(os.path.join('data', self.plan_id + '.csv'))
            my_camp = camps[camps['camp_name'] == self.camp_name]
            print("\nCurrent capacity of " + self.camp_name + ": " + str(my_camp.iloc[0]['capacity']))
            print("The camp currently has " + str(my_camp.iloc[0]['refugees']) + " refugees.")

            logging.debug(f"{self.username} prompted to enter their camp's new capacity.")
            while True:
                print("Enter [X] to return to the previous step.\n")
                new_capacity = input(">>New capacity: ")
                if new_capacity.upper() == "X":
                    logging.debug("Returning to previous step.")
                    return
                try:
                    new_capacity = int(new_capacity)
                    if new_capacity < 1:
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a positive integer.")
                    logging.error("Invalid user input.")
                    continue
                if new_capacity < my_camp.iloc[0]['refugees']:
                    print("\nInvalid input: New capacity is less than refugee population. "
                          "\nPlease re-enter or return to the previous step.")
                    logging.error("Capacity entered is less than refugee population.")
                    continue
                if new_capacity == my_camp.iloc[0]['capacity']:
                    print("\nCapacity is unchanged. "
                          "Please try again or return to the previous step.")
                    logging.error("Capacity is unchanged.")
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'capacity'] = new_capacity
            camps.to_csv(os.path.join('data', self.plan_id + '.csv'), index=False)
            print("\nRefugee capacity updated successfully!")
            print("New refugee capacity:", new_capacity)
            logging.debug("camps csv file updated")
            return

        print("\n--------------------------------------------")
        print("\tUPDATE CAMP INFORMATION")
        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            # inner loop to catch invalid input
            logging.debug(f"{self.username} prompted to select which camp information to edit.")
            while True:
                print("\nWhich details would you like to update?")
                print("Enter [1] for refugee capacity")
                print("Enter [2] for consumption of food packets")
                print("Enter [3] for consumption of water portions")
                print("Enter [4] for use of first-aid kits")
                print("Enter [0] to return to the previous menu\n")
                try:
                    option = int(input(">>Select an option: "))
                    if option not in range(5):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break

            if option == 0:
                logging.debug(f"Finished updating camp information. Returning to the camp information menu.")
                return
            if option == 1:
                edit_capacity()
            if option == 2:
                resource_consumption.edit_food(self.plan_id, self.camp_name)
            if option == 3:
                resource_consumption.edit_water(self.plan_id, self.camp_name)
            if option == 4:
                resource_consumption.edit_medical_supplies(self.plan_id, self.camp_name)

    def add_volunteering_session(self):
        """
        Enables the volunteer to add a volunteering session for themselves.
        The volunteer is prompted for the date, start time and end time of the session.
        """
        print("\n--------------------------------------------")
        print("\tADD VOLUNTEERING SESSION")
        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        cur_user_times = vol_times[vol_times['username'] == self.username]
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

        logging.debug(f"{self.username} has finished entering details of new volunteering session.")
        # update csv file
        vol_times = open(os.path.join('data', 'volunteering_times.csv'), "a")
        vol_times.write(f'\n{self.username},{self.plan_id},{self.camp_name},{start_time},{end_time}')
        vol_times.close()
        logging.debug("volunteering_times.csv updated")
        print("\nVolunteering session added successfully!")
        return

    def view_volunteering_sessions(self):
        """Enables the volunteer to view all volunteering sessions they have scheduled."""
        print("\n--------------------------------------------")
        print("\tVIEW VOLUNTEERING SESSIONS")
        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        cur_user_times = vol_times[vol_times['username'] == self.username]
        if len(cur_user_times.index) == 0:
            print("You do not have any volunteering sessions.")
            logging.info(f"{self.username} does not have any volunteering sessions.")
            return

        logging.debug(f"Displaying {self.username}'s volunteering sessions.")
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])
        print("You have added the following volunteering sessions:")
        for row in range(len(cur_user_times.index)):
            print(str(row+1) + ".", "Start:", datetime.datetime.strptime(cur_user_times['start_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"),
                  "\t", "End:", datetime.datetime.strptime(cur_user_times['end_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"))
        return

    def remove_volunteering_session(self):
        """Enables the volunteer to remove a volunteering sessions they have scheduled."""
        print("\n--------------------------------------------")
        print("\tREMOVE VOLUNTEERING SESSION")
        vol_times = pd.read_csv(os.path.join('data', 'volunteering_times.csv'))
        cur_user_times = vol_times[vol_times['username'] == self.username]
        if len(cur_user_times.index) == 0:
            print("You do not have any volunteering sessions.")
            logging.warning(f"{self.username} does not have any volunteering sessions.")
            return
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])

        logging.debug(f"{self.username} prompted to select a volunteering session to remove.")
        while True:
            print("Your volunteering sessions:")
            for row in range(len(cur_user_times.index)):
                start = datetime.datetime.strptime(cur_user_times['start_time'].iloc[row], '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
                end = datetime.datetime.strptime(cur_user_times['end_time'].iloc[row], '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
                print("[" + str(row + 1) + "]", "Start:", start, "\t", "End:", end)
            print("Enter [X] to return to the previous menu.\n")
            remove = input(">>Enter the number of the session you would like to remove: ").strip()
            if remove.upper() == "X":
                logging.debug("Returning to previous menu.")
                return
            try:
                remove = int(remove)
                if remove not in range(1, len(cur_user_times.index) + 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number corresponding to one of your volunteering sessions.\n")
                logging.error("Invalid user input.")
                continue

            # confirmation
            start = datetime.datetime.strptime(cur_user_times['start_time'].iloc[remove-1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            end = datetime.datetime.strptime(cur_user_times['end_time'].iloc[remove-1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            logging.debug(f"{self.username} prompted to confirm removal of volunteering session.")
            while True:
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
            vol_times = vol_times.drop(vol_times[(vol_times['username'] == self.username) &
                                                 (vol_times['start_time'] == cur_user_times['start_time'].iloc[remove-1])].index)
            vol_times.to_csv(os.path.join('data', 'volunteering_times.csv'), index=False)
            logging.debug("volunteering_times.csv updated")
            print("Volunteering session has been removed successfully.")
            return

    def request_resources(self):
        """
        Enables the volunteer to send a resource request to the admin.
        The volunteer is prompted to enter the number of food packets, water portions and first-aid kits requested in turn.
        """
        print("\n--------------------------------------------")
        print("\t\tREQUEST RESOURCES")
        print("You are requesting resources for", self.camp_name, "at plan", self.plan_id)
        camps = pd.read_csv(os.path.join('data', self.plan_id + '.csv'))
        my_camp = camps[camps['camp_name'] == self.camp_name]
        print("Your camp's current resources:")
        print("Food packets:", my_camp.iloc[0]['food'])
        print("Water portions:", my_camp.iloc[0]['water'])
        print("First-aid kits:", my_camp.iloc[0]['firstaid_kits'])

        progress = 0
        while progress <= 3:
            if progress == 0:
                logging.debug(f"{self.username} prompted to enter number of food packets requested.")
                while True:
                    print("\nEnter [X] to return to the previous menu.\n")
                    food = input(">>Enter the number of food packets you are requesting: ")
                    if food.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    try:
                        food = int(food)
                        if food < 0:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a non-negative integer.")
                        logging.error("Invalid user input.")
                        continue
                    progress += 1
                    break

            if progress == 1:
                logging.debug(f"{self.username} prompted to enter number of water portions requested.")
                while True:
                    print("\nEnter [X] to return to the previous menu or [B] to return to the previous step.\n")
                    water = input(">>Enter the number of water portions you are requesting: ")
                    if water.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    if water.upper() == "B":
                        logging.debug("Returning to previous step.")
                        progress -= 1
                        break
                    try:
                        water = int(water)
                        if water < 0:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a non-negative integer.")
                        logging.error("Invalid user input.")
                        continue
                    progress += 1
                    break

            if progress == 2:
                logging.debug(f"{self.username} prompted to enter number of first-aid kits requested.")
                while True:
                    print("\nEnter [X] to return to the previous menu or [B] to return to the previous step.\n")
                    kits = input(">>Enter the number of first-aid kits you are requesting: ")
                    if kits.upper() == "X":
                        logging.debug("Returning to previous menu.")
                        return
                    if kits.upper() == "B":
                        logging.debug("Returning to previous step.")
                        progress -= 1
                        break
                    try:
                        kits = int(kits)
                        if kits < 0:
                            raise ValueError
                    except ValueError:
                        print("\nPlease enter a non-negative integer.")
                        logging.error("Invalid user input.")
                        continue
                    progress += 1
                    break

            if progress == 3: # check that not all requested resources are 0
                if food == 0 and water == 0 and kits == 0:
                    print("\nYou cannot request 0 of all resources. Please enter your request again.")
                    logging.error(f"{self.username} requested 0 of all resources. "
                                  f"They will be prompted to re-enter the request.")
                    progress = 0
                else:
                    progress += 1

        # collected data
        data = {
            'username': [self.username],
            'plan_id': [self.plan_id],
            'camp_name': [self.camp_name],
            'food': [food],
            'water': [water],
            'firstaid_kits': [kits],
            'resolved': 0
        }
        df = pd.DataFrame(data)

        try:
            existing_df = pd.read_csv(os.path.join('data', 'resource_requests.csv'))
        except FileNotFoundError:
            df.to_csv(os.path.join('data', 'resource_requests.csv'), index=False)
            logging.info(f"{self.username} requests for more resources while no file found.\nNew csv file is created.")
            print("\nYour request is recorded successfully.\n"
                  "An administrator will respond to your request shortly.")
            return
        # Append the new data
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(os.path.join('data', 'resource_requests.csv'), index=False)
        logging.debug("Resource request complete.")
        logging.debug("resource_requests.csv updated")

        print("\nYour request is recorded successfully.\n"
              "An administrator will respond to your request shortly.")
        return
