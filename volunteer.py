import pandas as pd, numpy as np, re, datetime
from coded_vars import convert_gender, convert_medical_condition
import refugee_profile_funcs, volunteering_session_funcs
import logging

class Volunteer:
    """Class for Volunteer users. Initialised when a user successfully logs in as a volunteer."""
    def __init__(self, username, password, first_name, last_name, email, phone_number, gender, date_of_birth, plan_id, camp_name):
        """Initialise attributes with the user's details."""
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
        while self.logged_in:
            print("\n---------------")
            print("Volunteer Menu")
            print("---------------")
            while True:
                print("What would you like to do,", self.first_name, self.last_name + "?")
                print("Enter [1] for personal information and camp identification")
                print("Enter [2] to create, view, edit or remove a refugee profile")
                print("Enter [3] to display or update your camp's information")
                print("Enter [4] to request account deactivation")
                print("Enter [5] to add, view or remove volunteering sessions")
                print("Enter [0] to logout")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(6):
                        logging.error(f"Value error raised - {self.username} entered {option}")
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"{self.username} has chosen to logout.")
                self.logout()
            if option == 1:
                logging.debug(f"{self.first_name} {self.last_name} has selected personal menu.")
                self.personal_menu()
            if option == 2:
                logging.debug(f"{self.username} has selected refugee menu.")
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
        while True:
            print("\nPersonal Information and Camp Identification")
            while True:
                print("Enter [1] to view your personal information")
                print("Enter [2] to edit your personal information")
                print("Enter [3] to update your camp identification")
                print("Enter [0] to return to the volunteer menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    logging.debug(f'{self.username} has entered {user_input}.')
                    if option not in range(4):
                        logging.error(f"{self.username} has entered {user_input}, raising a ValueError.")
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"{self.username} has returned to the volunteer menu.")
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
        while True:
            print("\nManage Refugee Profiles")
            if not self.camp_name:
                logging.debug(f"{self.username} does not have a camp on their profile.")
                print("\nVolunteers can only manage refugee profiles for their current camp. Please add your camp identification.")
                return

            while True:
                print("Enter [1] to create a new refugee profile")
                print("Enter [2] to view a refugee profile")
                print("Enter [3] to edit or remove a refugee profile")
                print("Enter [0] to return to the volunteer menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(4):
                        logging.error(f'{self.username} did not select a valid option at the Refugee Profile menu.')
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f"{self.username} has returned to the volunteer menu.")
                return
            if option == 1:
                logging.debug(f'{self.username} will be taken to the create refugee profile function.')
                self.create_refugee_profile()
            if option == 2:
                logging.debug(f'{self.username} will be taken to the view refugee profile function.')
                self.view_refugee_profile()
            if option == 3:
                logging.debug(f'{self.username} will be taken to the edit refugee profile function.')
                self.edit_refugee_profile()

    def camp_info_menu(self):
        while True:
            print("\nCamp Information")
            if not self.camp_name:
                print("\nPlease add your camp identification in order to display or update camp information.")
                return

            while True:
                print("Enter [1] to display your camp's information")
                print("Enter [2] to update your camp's information")
                print("Enter [0] to return to the volunteer menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(3):
                        logging.error(f'{self.username} has entered {option} which is not an option on the camp information menu.')
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                logging.debug(f'{self.username} has returned to the volunteer menu.')
                return
            if option == 1:
                logging.debug(f'{self.username} has chosen to display camp information.')
                self.display_camp_info()
            if option == 2:
                logging.debug(f'{self.username} has chosen to update camp information.')
                self.update_camp_info()

    def volunteering_session_menu(self):
        while True:
            print("\nManage Volunteering Times")
            print("Tell us when you are coming to volunteer.")
            if not self.camp_name:
                print("\nPlease add your camp identification in order to manage volunteering times.")
                return

            while True:
                print("Enter [1] to add a volunteering session")
                print("Enter [2] to view your volunteering sessions")
                print("Enter [3] to remove a volunteering session")
                print("Enter [0] to return to the volunteer menu")
                try:
                    user_input = input("Select an option: ")
                    option = int(user_input)
                    if option not in range(4):
                        logging.error(f'{self.username} has entered {user_input}, which raised a ValueError.')
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
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
        logging.info(f'{self.username} has logged out of their session.')
        self.logged_in = False
        print("You are now logged out. See you again!")

    def request_deactivation(self):
        print("\nRequest account deactivation")
        while True:
            print("Are you sure you would like to deactivate your account?")
            print("If your request is approved, you will no longer be able to volunteer at humanitarian plans or login to the system.")
            print("To reactivate your account subsequently, you will need to contact an administrator.")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the volunteer menu")
            try:
                user_input = input("Select an option: ")
                option = int(user_input)
                if option not in (0, 1):
                    logging.error(f'{self.username} has entered {user_input} when trying to deactivate their account. ValueError raised.')
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.\n")
                continue
            break
        if option == 0:
            logging.debug(f'{self.username} has returned to the volunteer menu from the "request deactivation" menu.')
            return

        # update csv files
        users = pd.read_csv('users.csv', dtype={'password': str})
        cur_user = (users['username'] == self.username)
        users.loc[cur_user, 'deactivation_requested'] = 1
        users.to_csv('users.csv', index=False)
        logging.info(f"{self.username}'s request to deactivate their account has been updated on the users.csv file.")

        print("Your request to deactivate your account has been registered.")
        print("An administrator will respond to your request shortly.")
        logging.debug(f"{self.username} has been informed that their request for deactivation has been passed to an administrator.")
        return

    def view_personal_info(self):
        """
        Displays the user's details when called, except camp identification and password.
        Additional option to allow user to view password.
        """
        gender_str = convert_gender(self.gender)

        print("\nView personal information")
        print("Your details are as follows:")
        print("Username:", self.username)
        print("First name:", self.first_name)
        print("Last name:", self.last_name)
        print("Email:", self.email)
        print("Phone number:", self.phone_number)
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", self.date_of_birth)

        logging.debug(f"{self.username}'s personal information has been displayed.")

        while True:
            print("\nEnter [1] if you would like to view your password. The password will appear in plain text.")
            print("Enter [0] to return to the previous menu")
            try:
                user_input = input("Select an option: ")
                option = int(user_input)
                if option not in (0, 1):
                    logging.error(f"{self.username} has entered {user_input} when trying to view their password. They should have entered either 0 or 1. A ValueError has been raised.")
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 1:
            logging.debug(f"{self.username} has chosen to view their password.")
            print("Your password is:", self.password)
            input("Press Enter to return to the previous menu. ")
        # back to volunteer_menu() loop while logged in
        return

    def edit_personal_info(self):
        def edit_username():
            print("\nYour current username is:", self.username)
            logging.debug(f"{self.username} has been shown their current username.")
            while True:
                print("Enter [0] to return to previous step.")
                new_username = input("Enter new username: ").strip()
                if new_username == "0":
                    return
                if new_username == self.username:
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
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'username'] = new_username
            users.to_csv('users.csv', index=False)
            print("Your new username is:", new_username)
            self.username = new_username
            return

        def edit_password():
            print("\nYour current password is:", self.password)
            while True:
                print("Enter [0] to return to the previous step.")
                new_password = input("Enter new password: ")
                if new_password == "0":
                    return
                if new_password == self.password:
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
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'password'] = new_password
            users.to_csv('users.csv', index=False)
            print("Your new password is:", new_password)
            self.password = new_password
            return

        def edit_first_name():
            print("\nYour current first name is:", self.first_name)
            while True:
                print("Enter [0] to return to the previous step.")
                new_fname = input("Enter new first name: ").strip()
                if new_fname == "0":
                    return
                if new_fname == self.first_name:
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
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'first_name'] = new_fname
            users.to_csv('users.csv', index=False)
            print("You have changed your first name to:", new_fname)
            self.first_name = new_fname
            return

        def edit_last_name():
            print("\nYour current last name is:", self.last_name)
            while True:
                print("Enter [0] to return to the previous step.")
                new_lname = input("Enter new last name: ").strip()
                if new_lname == "0":
                    return
                if new_lname == self.last_name:
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
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'last_name'] = new_lname
            users.to_csv('users.csv', index=False)
            print("You have changed your last name to:", new_lname)
            self.last_name = new_lname
            return

        def edit_gender():
            gender_str = convert_gender(self.gender)

            print("\nYour current gender is:", gender_str)
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
                    print("Please enter a number from the options provided.\n")
                    continue
                if new_gender == 0:
                    return
                if new_gender == self.gender:
                    print("New gender is the same as current gender. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            users = pd.read_csv('users.csv', dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'gender'] = new_gender
            users.to_csv('users.csv', index=False)

            new_gender_str = convert_gender(new_gender)
            print("You have changed your gender to:", new_gender_str)
            self.gender = new_gender
            return

        def edit_email():
            print("\nYour current email address is:", self.email)
            while True:
                print("Enter [0] to return to the previous step.")
                new_email = input("Enter new email address: ").strip()
                if new_email == "0":
                    return
                if new_email == self.email:
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
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'email'] = new_email
            users.to_csv('users.csv', index=False)
            print("You have changed your email address to:", new_email)
            self.email = new_email
            return

        def edit_phone_num():
            print("\nYour current phone number is:", self.phone_number)
            while True:
                print("Enter [0] to return to the previous step.")
                new_phone_num = input("Enter new phone number: ").strip()
                if new_phone_num == "0":
                    return
                if new_phone_num == self.phone_number:
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
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'phone_number'] = new_phone_num
            users.to_csv('users.csv', index=False)
            print("You have changed your phone number to:", new_phone_num)
            self.phone_number = new_phone_num
            return

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            # inner loop to catch invalid input
            while True:
                print("\nEdit personal information")
                print("Which details would you like to update?")
                print("Enter [1] for username")
                print("Enter [2] for password")
                print("Enter [3] for first name")
                print("Enter [4] for last name")
                print("Enter [5] for gender")
                print("Enter [6] for email")
                print("Enter [7] for phone number")
                print("Enter [0] to return to the previous menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(8):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break

            if option == 0:
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
        def add_camp(plan_id):
            camps = pd.read_csv(plan_id + '.csv')
            while True:
                print("Enter [X] to return to the previous menu.")
                print("Choose a camp.")
                print("\nCamp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                camp_num = input("Enter the number of the camp you would like to join (e.g. [1] for Camp 1): ")
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

        def edit_camp(plan_id):
            camps = pd.read_csv(plan_id + '.csv')
            if len(camps.index) == 1:
                print("There is currently only one camp. It is not possible to change camp identification.")
                return self.camp_name

            while True:
                print("Enter [X] to return to the previous menu.")
                print("Choose a new camp.")
                print("\nCamp Name - # Volunteers - # Refugees - Capacity")
                for row in range(len(camps.index)):
                    print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
                          str(camps['refugees'].iloc[row]) + " refugees",
                          str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                camp_num = input("Enter the number of the camp you would like to join (e.g. [1] for Camp 1): ")
                if camp_num == "X":
                    return self.camp_name
                try:
                    camp_num = int(camp_num)
                    if camp_num not in range(1, len(camps.index) + 1):
                        raise ValueError
                except ValueError:
                    print("Please enter the number of a camp from the list displayed.")
                    continue
                new_camp = "Camp " + str(camp_num)
                if new_camp == self.camp_name:
                    print("New camp is the same as current camp. Please try again or return to the previous menu.\n")
                    continue
                return new_camp

        print("\nYou are volunteering at plan ID:", self.plan_id)
        print("Your current camp is:", self.camp_name)
        if not self.camp_name:
            new_camp = add_camp(self.plan_id)
        else:
            while True:
                print("Enter [1] to update camp identification")
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
                    new_camp = edit_camp(self.plan_id)
                if option == 2:
                    while True:
                        print("Are you sure you would like to remove your camp identification?")
                        print("All your volunteering sessions will be erased.")
                        print("Enter [1] to proceed")
                        print("Enter [0] to go back to the previous step")
                        try:
                            remove_option = int(input("Select an option: "))
                            if remove_option not in (0, 1):
                                raise ValueError
                        except ValueError:
                            print("Please enter a number from the options provided.\n")
                            continue
                        break
                    if remove_option == 0:
                        continue
                    new_camp = None
                break

        # update csv files
        if new_camp != self.camp_name:
            users = pd.read_csv('users.csv', dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'camp_name'] = new_camp
            users.to_csv('users.csv', index=False)

            camps = pd.read_csv(self.plan_id + '.csv')
            if new_camp:
                chosen = (camps['camp_name'] == new_camp)
                camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            if self.camp_name:
                old = (camps['camp_name'] == self.camp_name)
                camps.loc[old, 'volunteers'] = camps.loc[old, 'volunteers'] - 1
            camps.to_csv(self.plan_id + '.csv', index=False)

            if self.camp_name and not new_camp: # remove volunteering sessions
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times = vol_times.drop(vol_times[vol_times['username'] == self.username].index)
                vol_times.to_csv('volunteering_times.csv', index=False)
            if self.camp_name and new_camp: # change camp_name in volunteering_times.csv
                vol_times = pd.read_csv("volunteering_times.csv")
                vol_times.loc[vol_times["username"] == self.username, "camp_name"] = new_camp
                vol_times.to_csv('volunteering_times.csv', index=False)

            print("Your new camp is:", new_camp)
            self.camp_name = new_camp
        return

    def create_refugee_profile(self):
        """
        This method lets the volunteer create a new refugee profile.
        The volunteer needs to input the refugee's name, date of birth, camp, medical condition, no. of family members and any other remarks.
        The refugee's details are then added to the file 'refugees.csv'.
        """
        def add_name():
            while True:
                print("\nEnter [0] to return to the previous menu.")
                refugee_name = input("Enter refugee name: ").strip()
                if refugee_name == "0":
                    return refugee_name
                # validation
                if refugee_name == "":
                    print("Please enter a refugee name.")
                    continue
                s = re.search("^[A-Z][a-zA-Z-' ]*$", refugee_name)
                if not s:
                    print(
                        "Name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
                    continue
                return refugee_name

        print("\nAdd refugee profile")
        camps = pd.read_csv(self.plan_id + '.csv')
        cur_camp = camps[camps['camp_name'] == self.camp_name]
        remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']

        if remaining_cap == 0:
            print("\nYour camp has reached its maximum capacity. Unable to add new refugees.")
            return
        print("\nYour camp's remaining capacity is " + str(remaining_cap) + ".")
        print("Please return to the previous menu if the refugee's family is larger than this number.")

        progress = 0
        # loop allowing user to go back
        while progress < 6:
            if progress == 0:
                refugee_name = add_name()
                if refugee_name == "0":
                    return
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
                   'date_of_birth': [date_of_birth], 'plan_id': [self.plan_id], 'camp_name': [self.camp_name],
                   'medical_condition': [medical_cond], 'family_members': [family], 'remarks': [remarks]}
        new = pd.DataFrame(new_row)
        refugees = pd.concat([refugees, new], ignore_index=True)
        refugees.to_csv('refugees.csv', index=False)

        camps = pd.read_csv(self.plan_id + '.csv')
        chosen = (camps['camp_name'] == self.camp_name)
        camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] + family
        camps.to_csv(self.plan_id + '.csv', index=False)

        # Print details provided
        gender_str = convert_gender(gender)
        medical_str = convert_medical_condition(medical_cond)

        print("\nRefugee profile created! The refugee and their family members have been added to " + self.camp_name + ".")
        print("You have entered the following details:")
        print("Refugee name:", refugee_name)
        print("Gender:", gender_str)
        print("Date of birth:", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        return

    def view_refugee_profile(self):
        """
        Prompts the user for the refugee ID, then prints the refugee's details.
        """
        print("\nView refugee profile")
        refugees = pd.read_csv('refugees.csv')
        refugees = refugees[(refugees['plan_id'] == self.plan_id) & (refugees['camp_name'] == self.camp_name)]
        if len(refugees.index) == 0:
            print("There are no refugees at your current camp.")
            return

        refugees = refugees.replace({np.nan: None})
        print("You will be prompted for the refugee ID of the refugee whose profile you would like to view.")
        while True:
            print("Enter [1] to proceed")
            print("Enter [2] to list all refugees at your current camp")
            print("Enter [0] to return to the previous menu")
            try:
                option = int(input("Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 0:
            return
        if option == 2: # list refugees at volunteer's camp
            print("\nRefugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")

        # Obtain refugee ID
        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                refugee_id = int(input("Enter refugee ID: "))
                if refugee_id == 0:
                    return
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("Please enter a refugee ID corresponding to a refugee in your camp.")
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

        print("Details of refugee ID:", refugee_id)
        print("Camp name:", self.camp_name)
        print("Refugee name:", refugee_name)
        print("Gender:", gender_str)
        print("Date of birth (DD-MM-YYYY):", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        return

    def edit_refugee_profile(self):
        print("\nEdit or remove refugee profile")
        refugees = pd.read_csv('refugees.csv')
        refugees = refugees[(refugees['plan_id'] == self.plan_id) & (refugees['camp_name'] == self.camp_name)]
        if len(refugees.index) == 0:
            print("There are no refugees at your current camp.")
            return

        refugees = refugees.replace({np.nan: None})
        print("You will be prompted for the refugee ID of the refugee whose profile you would like to edit.")
        while True:
            print("Enter [1] to proceed")
            print("Enter [2] to list all refugees at your current camp")
            print("Enter [0] to return to the previous menu")
            try:
                option = int(input("Select an option: "))
                if option not in (0, 1, 2):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 0:
            return
        if option == 2: # list refugees at volunteer's camp
            print("\nRefugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")

        # Obtain refugee ID
        while True:
            print("\nEnter [0] to return to the previous menu.")
            try:
                refugee_id = int(input("Enter refugee ID: "))
                if refugee_id == 0:
                    return
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("Please enter a refugee ID corresponding to a refugee in your camp.")
                continue
            break

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            refugees = pd.read_csv('refugees.csv')
            selected = refugees[refugees['refugee_id'] == refugee_id]
            selected = selected.replace({np.nan: None})
            refugee_name = selected.iloc[0]['refugee_name']
            gender = selected.iloc[0]['gender']
            medical_cond = selected.iloc[0]['medical_condition']
            family = selected.iloc[0]['family_members']
            remarks = selected.iloc[0]['remarks']
            # inner loop to catch invalid input
            while True:
                print("\nWhich details would you like to update?")
                print("Enter [1] for refugee name")
                print("Enter [2] for gender")
                print("Enter [3] for medical condition")
                print("Enter [4] for no. of family members")
                print("Enter [5] for remarks")
                print("Enter [9] to remove the refugee's profile")
                print("Enter [0] to return to the previous menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in (0,1,2,3,4,5,9):
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
                refugee_profile_funcs.edit_medical_cond(refugee_id, medical_cond)
            if option == 4:
                refugee_profile_funcs.edit_family(self.plan_id, self.camp_name, refugee_id, family)
            if option == 5:
                refugee_profile_funcs.edit_remarks(refugee_id, remarks)
            if option == 9:
                refugee_profile_funcs.remove_refugee(self.plan_id, self.camp_name, refugee_id, refugee_name, family)
                return

    def display_camp_info(self):
        print("\nDisplay camp information")
        camps = pd.read_csv(self.plan_id + '.csv')
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
        def edit_capacity():
            camps = pd.read_csv(self.plan_id + '.csv')
            my_camp = camps[camps['camp_name'] == self.camp_name]
            print("\nCurrent capacity of " + self.camp_name + ": " + str(my_camp.iloc[0]['capacity']))
            print("The camp currently has " + str(my_camp.iloc[0]['refugees']) + " refugees.")

            while True:
                print("\nEnter [X] to return to the previous step.")
                new_capacity = input("New capacity: ")
                if new_capacity == "X":
                    return
                try:
                    new_capacity = int(new_capacity)
                    if new_capacity < 1:
                        raise ValueError
                except ValueError:
                    print("Please enter a positive integer.")
                    continue
                if new_capacity < my_camp.iloc[0]['refugees']:
                    print("Invalid input: New capacity is less than refugee population. Please re-enter or return to the previous step.")
                    continue
                if new_capacity == my_camp.iloc[0]['capacity']:
                    print("Capacity is unchanged. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'capacity'] = new_capacity
            camps.to_csv(self.plan_id + '.csv', index=False)
            print("New refugee capacity:", new_capacity)
            return

        def edit_food():
            camps = pd.read_csv(self.plan_id + '.csv')
            my_camp = camps[camps['camp_name'] == self.camp_name]
            cur_food = my_camp.iloc[0]['food']
            print("\nCurrent supply of food packets at " + self.camp_name + ": " + str(cur_food))

            while True:
                print("\nEnter [X] to return to the previous step.")
                food_consumed = input("Enter the number of food packets consumed: ")
                if food_consumed == "X":
                    return
                try:
                    food_consumed = int(food_consumed)
                    if food_consumed <= 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a positive integer.")
                    continue
                if food_consumed > cur_food:
                    print("Food consumed exceeds the current supply. Please try again or return to the previous step.")
                    continue

                # confirmation
                while True:
                    print("\nConfirmation:", food_consumed, "out of", cur_food, "food packets have been consumed.")
                    print("Proceed to update camp information?")
                    print("Enter [1] to proceed")
                    print("Enter [0] to return to the previous step")
                    try:
                        confirm = int(input("Select an option: "))
                        if confirm not in (0, 1):
                            raise ValueError
                    except ValueError:
                        print("Please enter a number from the options provided.")
                        continue
                    break
                if confirm == 0:
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'food'] = cur_food - food_consumed
            camps.to_csv(self.plan_id + '.csv', index=False)
            print("Updated supply of food packets:", cur_food - food_consumed)
            return

        def edit_water():
            camps = pd.read_csv(self.plan_id + '.csv')
            my_camp = camps[camps['camp_name'] == self.camp_name]
            cur_water = my_camp.iloc[0]['water']
            print("\nCurrent supply of water portions at " + self.camp_name + ": " + str(cur_water))

            while True:
                print("\nEnter [X] to return to the previous step.")
                water_consumed = input("Enter the number of water portions consumed: ")
                if water_consumed == "X":
                    return
                try:
                    water_consumed = int(water_consumed)
                    if water_consumed <= 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a positive integer.")
                    continue
                if water_consumed > cur_water:
                    print("Water consumed exceeds the current supply. Please try again or return to the previous step.")
                    continue

                # confirmation
                while True:
                    print("\nConfirmation:", water_consumed, "out of", cur_water, "water portions have been consumed.")
                    print("Proceed to update camp information?")
                    print("Enter [1] to proceed")
                    print("Enter [0] to return to the previous step")
                    try:
                        confirm = int(input("Select an option: "))
                        if confirm not in (0, 1):
                            raise ValueError
                    except ValueError:
                        print("Please enter a number from the options provided.")
                        continue
                    break
                if confirm == 0:
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'water'] = cur_water - water_consumed
            camps.to_csv(self.plan_id + '.csv', index=False)
            print("Updated supply of water portions:", cur_water - water_consumed)
            return

        def edit_medical_supplies():
            camps = pd.read_csv(self.plan_id + '.csv')
            my_camp = camps[camps['camp_name'] == self.camp_name]
            cur_medical = my_camp.iloc[0]['firstaid_kits']
            print("\nCurrent supply of first-aid kits at " + self.camp_name + ": " + str(cur_medical))

            while True:
                print("\nEnter [X] to return to the previous step.")
                medical_used = input("Enter the number of first-aid kits used: ")
                if medical_used == "X":
                    return
                try:
                    medical_used = int(medical_used)
                    if medical_used <= 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a positive integer.")
                    continue
                if medical_used > cur_medical:
                    print("First-aid kits used exceed the current supply. Please try again or return to the previous step.")
                    continue

                # confirmation
                while True:
                    print("\nConfirmation:", medical_used, "out of", cur_medical, "first-aid kits have been used.")
                    print("Proceed to update camp information?")
                    print("Enter [1] to proceed")
                    print("Enter [0] to return to the previous step")
                    try:
                        confirm = int(input("Select an option: "))
                        if confirm not in (0, 1):
                            raise ValueError
                    except ValueError:
                        print("Please enter a number from the options provided.")
                        continue
                    break
                if confirm == 0:
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'firstaid_kits'] = cur_medical - medical_used
            camps.to_csv(self.plan_id + '.csv', index=False)
            print("Updated supply of first-aid kits:", cur_medical - medical_used)
            return

        print("\nUpdate camp information")
        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            # inner loop to catch invalid input
            while True:
                print("\nWhich details would you like to update?")
                print("Enter [1] for refugee capacity")
                print("Enter [2] for consumption of food packets")
                print("Enter [3] for consumption of water portions")
                print("Enter [4] for use of first-aid kits")
                print("Enter [0] to return to the previous menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(5):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break

            if option == 0:
                return
            if option == 1:
                edit_capacity()
            if option == 2:
                edit_food()
            if option == 3:
                edit_water()
            if option == 4:
                edit_medical_supplies()

    def add_volunteering_session(self):
        print("\nAdd a volunteering session")
        vol_times = pd.read_csv("volunteering_times.csv")
        cur_user_times = vol_times[vol_times['username'] == self.username]
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
        vol_times.write(f'\n{self.username},{self.plan_id},{self.camp_name},{start_time},{end_time}')
        vol_times.close()
        print("Volunteering session added successfully!")
        return

    def view_volunteering_sessions(self):
        print("\nView volunteering sessions")
        vol_times = pd.read_csv("volunteering_times.csv")
        cur_user_times = vol_times[vol_times['username'] == self.username]
        if len(cur_user_times.index) == 0:
            print("You do not have any volunteering sessions.")
            return

        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])
        print("You have added the following volunteering sessions:")
        for row in range(len(cur_user_times.index)):
            print(str(row+1) + ".", "Start:", datetime.datetime.strptime(cur_user_times['start_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"),
                  "\t", "End:", datetime.datetime.strptime(cur_user_times['end_time'].iloc[row], "%Y-%m-%d %H:%M").strftime("%d-%m-%Y %H:%M"))
        return

    def remove_volunteering_session(self):
        print("\nRemove a volunteering session")
        vol_times = pd.read_csv("volunteering_times.csv")
        cur_user_times = vol_times[vol_times['username'] == self.username]
        if len(cur_user_times.index) == 0:
            print("You do not have any volunteering sessions.")
            return
        # sort existing times by ascending start time (need date in YYYY-MM-DD format)
        cur_user_times = cur_user_times.sort_values(by=['start_time'])

        while True:
            print("Enter [X] to return to the previous menu.")
            print("Your volunteering sessions:")
            for row in range(len(cur_user_times.index)):
                start = datetime.datetime.strptime(cur_user_times['start_time'].iloc[row], '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
                end = datetime.datetime.strptime(cur_user_times['end_time'].iloc[row], '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
                print("[" + str(row + 1) + "]", "Start:", start, "\t", "End:", end)
            remove = input("Enter the number of the session you would like to remove: ").strip()
            if remove == "X":
                return
            try:
                remove = int(remove)
                if remove not in range(1, len(cur_user_times.index) + 1):
                    raise ValueError
            except ValueError:
                print("Please enter a number corresponding to one of your volunteering sessions.")
                continue

            # confirmation
            start = datetime.datetime.strptime(cur_user_times['start_time'].iloc[remove-1], '%Y-%m-%d %H:%M').strftime(
                '%d-%m-%Y %H:%M')
            end = datetime.datetime.strptime(cur_user_times['end_time'].iloc[remove-1], '%Y-%m-%d %H:%M').strftime(
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
            vol_times = vol_times.drop(vol_times[(vol_times['username'] == self.username) &
                                                 (vol_times['start_time'] == cur_user_times['start_time'].iloc[remove-1])].index)
            vol_times.to_csv('volunteering_times.csv', index=False)
            print("Volunteering session has been removed.")
            return
