import pandas as pd, numpy as np, re, datetime
from coded_vars import convert_gender, convert_medical_condition

class Volunteer:
    """Class for Volunteer users. Initialised when a user successfully logs in as a volunteer."""
    def __init__(self, username, password, first_name, last_name, email, phone_number, gender, date_of_birth, camp_name):
        """Initialise attributes with the user's details."""
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.camp_name = camp_name
        self.logged_in = True

    def volunteer_menu(self):
        while self.logged_in:
            print("\n---------------")
            print("Volunteer Menu")
            print("---------------")
            while True:
                print("What would you like to do,", self.first_name, self.last_name + "?")
                print("Enter [1] to view your personal information")
                print("Enter [2] to edit your personal information")
                print("Enter [3] to update your camp identification")
                print("Enter [4] to create a refugee profile")
                print("Enter [5] to view a refugee profile")
                print("Enter [6] to edit or remove a refugee profile")
                print("Enter [7] to display your camp's information")
                print("Enter [8] to update your camp's information")
                # print("Enter [9] to add or manage a booking slot for volunteering")
                print("Enter [0] to logout")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if option == 0:
                self.logout()
            if option == 1:
                self.view_personal_info()
            if option == 2:
                self.edit_personal_info()
            if option == 3:
                self.update_camp()
            if option == 4:
                self.create_refugee_profile()
            if option == 5:
                self.view_refugee_profile()
            if option == 6:
                self.edit_refugee_profile()
            if option == 7:
                self.display_camp_info()
            if option == 8:
                self.update_camp_info()

    def logout(self):
        self.logged_in = False
        print("You are now logged out. See you again!\n")

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
        print("Date of birth:", self.date_of_birth)

        while True:
            print("\nEnter [1] if you would like to view your password. The password will appear in plain text.")
            print("Enter [0] to return to the volunteer menu")
            try:
                option = int(input("Select an option: "))
                if option not in (0, 1):
                    raise ValueError
            except ValueError:
                print("Please enter a number from the options provided.")
                continue
            break
        if option == 1:
            print("Your password is:", self.password)
            input("Press Enter to return to the volunteer menu. ")
        # back to volunteer_menu() loop while logged in
        return

    def edit_personal_info(self):
        def edit_username():
            print("\nYour current username is:", self.username)
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
                print("Enter [0] to return to the volunteer menu")
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
        def add_camp():
            plans = pd.read_csv('plans.csv')
            plans = plans[plans['end_date'].isna()]  # only show plans that haven't been closed

            if len(plans.index) == 0:
                print("No ongoing plans. It is not possible to add camp identification at the moment.")
                return None

            camps = pd.read_csv('camps.csv')
            plans_camps = pd.merge(plans, camps, how="inner", on="plan_name")
            plans_camps = plans_camps[
                ['camp_name', 'plan_name', 'description', 'location', 'volunteers', 'refugees', 'capacity']]

            while True:
                print("Enter [0] to return to the volunteer menu.")
                print("Choose a camp.")
                # print(plans_camps)
                print("\nCamp Name - Plan Name - Location - Description - # Volunteers - # Refugees - Capacity")
                for row in range(len(plans_camps.index)):
                    print(plans_camps['camp_name'].iloc[row], plans_camps['plan_name'].iloc[row],
                          plans_camps['location'].iloc[row], plans_camps['description'].iloc[row],
                          str(plans_camps['volunteers'].iloc[row]) + " volunteers",
                          str(plans_camps['refugees'].iloc[row]) + " refugees",
                          str(plans_camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                new_camp = input("Enter the name of the camp you would like to join: ")
                if new_camp == "0":
                    return None
                if new_camp not in plans_camps['camp_name'].values:
                    print("Please enter the name of a camp from the list displayed.\n")
                    continue
                return new_camp

        def edit_camp():
            plans = pd.read_csv('plans.csv')
            plans = plans[plans['end_date'].isna()]  # only show plans that haven't been closed
            camps = pd.read_csv('camps.csv')
            if len(camps.index) == 0:
                print("There is currently only one camp. It is not possible to change camp identification.")
                return self.camp_name

            plans_camps = pd.merge(plans, camps, how="inner", on="plan_name")
            plans_camps = plans_camps[
                ['camp_name', 'plan_name', 'description', 'location', 'volunteers', 'refugees', 'capacity']]

            while True:
                print("Enter [0] to return to the volunteer menu.")
                print("Choose a camp.")
                # print(plans_camps)
                print("\nCamp Name - Plan Name - Location - Description - # Volunteers - # Refugees - Capacity")
                for row in range(len(plans_camps.index)):
                    print(plans_camps['camp_name'].iloc[row], plans_camps['plan_name'].iloc[row],
                          plans_camps['location'].iloc[row], plans_camps['description'].iloc[row],
                          str(plans_camps['volunteers'].iloc[row]) + " volunteers",
                          str(plans_camps['refugees'].iloc[row]) + " refugees",
                          str(plans_camps['capacity'].iloc[row]) + " capacity", sep=" - ")
                new_camp = input("Enter the name of the camp you would like to join: ")
                if new_camp == "0":
                    return self.camp_name
                if new_camp not in plans_camps['camp_name'].values:
                    print("Please enter the name of a camp from the list displayed.\n")
                    continue
                if new_camp == self.camp_name:
                    print("New camp is the same as current camp. Please try again or return to the volunteer menu.\n")
                    continue
                return new_camp

        print("\nYour current camp is:", self.camp_name)
        if not self.camp_name:
            new_camp = add_camp()
        else:
            while True:
                print("Enter [1] to update camp identification")
                print("Enter [2] to remove camp identification")
                print("Enter [0] to return to the volunteer menu")
                try:
                    option = int(input("Select an option: "))
                    if option not in range(3):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                break
            if option == 0:
                return
            if option == 1:
                new_camp = edit_camp()
            if option == 2:
                new_camp = None

        # update csv files
        if new_camp != self.camp_name:
            users = pd.read_csv('users.csv', dtype={'password': str})
            cur_user = (users['username'] == self.username)
            users.loc[cur_user, 'camp_name'] = new_camp
            users.to_csv('users.csv', index=False)

            camps = pd.read_csv('camps.csv')
            if new_camp:
                chosen = (camps['camp_name'] == new_camp)
                camps.loc[chosen, 'volunteers'] = camps.loc[chosen, 'volunteers'] + 1
            if self.camp_name:
                old = (camps['camp_name'] == self.camp_name)
                camps.loc[old, 'volunteers'] = camps.loc[old, 'volunteers'] - 1
            camps.to_csv('camps.csv', index=False)

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
                print("\nEnter [0] to return to the volunteer menu.")
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

        def add_gender():
            while True:
                print("\nEnter [0] to return to the volunteer menu or [9] to go back to the previous step.")
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
                print("\nEnter [0] to return to the volunteer menu or [9] to go back to the previous step.")
                date_of_birth = input("Enter refugee's date of birth in the format YYYY-MM-DD: ")
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
                if t.year - dob.year > 121 or (t.year - dob.year == 121 and t.month > dob.month) or (
                        t.year - dob.year == 121 and t.month == dob.month and t.day >= dob.day):
                    while True:
                        print("\nWarning: Refugee is over 120 years old based on date of birth.")
                        print("Do you wish to proceed?")
                        print("Enter [1] to proceed")
                        print("Enter [9] to re-enter date of birth")
                        try:
                            overage_option = int(input("Select an option: "))
                            if overage_option not in (1, 9):
                                raise ValueError
                        except ValueError:
                            print("Please enter a number from the options provided.")
                            continue
                        break
                    if overage_option == 9:
                        continue
                return date_of_birth

        def add_medical_cond():
            while True:
                print("\nEnter [0] to return to the volunteer menu or [9] to go back to the previous step.")
                print("Medical condition:")
                print("Enter [1] for Healthy")
                print("Enter [2] for Minor illness with no injuries")
                print("Enter [3] for Major illness with no injuries")
                print("Enter [4] for Minor injury with no illness")
                print("Enter [5] for Major injury with no illness")
                print("Enter [6] for Illness and injury (non-critical)")
                print("Enter [7] for Critical condition (illness and/or injury)")
                try:
                    medical_cond = int(input("Select an option: "))
                    if medical_cond not in (0, 1, 2, 3, 4, 5, 6, 7, 9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    continue
                return medical_cond

        def add_family():
            while True:
                print("\nEnter [X] to return to the volunteer menu or [B] to go back to the previous step.")
                family = input("Number of family members: ")
                if family in ("X", "B"):
                    return family
                try:
                    family = int(family)
                    if family < 1:
                        raise ValueError
                except ValueError:
                    print("Please enter a positive integer.")
                    continue
                if family > remaining_cap:
                    print("Number of family members exceeds camp's capacity. Please re-enter or return to the volunteer menu.")
                    continue
                if family > 12:
                    while True:
                        print("\nWarning: Refugee's family has more than 12 members based on input.")
                        print("Do you wish to proceed?")
                        print("Enter [1] to proceed")
                        print("Enter [9] to re-enter number of family members")
                        try:
                            largefam_option = int(input("Select an option: "))
                            if largefam_option not in (1, 9):
                                raise ValueError
                        except ValueError:
                            print("Please enter a number from the options provided.")
                            continue
                        break
                    if largefam_option == "9":
                        continue
                return family

        def add_remarks():
            while True:
                print("\nEnter [0] to return to the volunteer menu or [9] to go back to the previous step.")
                try:
                    remarks = input("Enter additional remarks (optional, max 200 characters): ").strip()
                    if remarks in ("0", "9"):
                        return remarks
                    s = re.search("[a-zA-Z]", remarks)
                    if remarks != "" and not s:
                        raise ValueError
                except ValueError:
                    print("Please ensure remarks contain text.")
                    continue
                if len(remarks) > 200:
                    print("Remarks cannot exceed 200 characters.")
                    continue
                return remarks


        # Volunteer can only add refugee profile for their current camp if they have camp identification
        if not self.camp_name:
            print("\nVolunteers can only add refugee profiles to their current camp. Please add your camp identification.")
            return

        print("\nAdd refugee profile")
        camps = pd.read_csv('camps.csv')
        cur_camp = camps[camps['camp_name'] == self.camp_name]
        remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']

        if remaining_cap == 0:
            print("\nYour camp has reached its maximum capacity. Unable to add new refugees.")
            return
        print("\nYour camp's remaining capacity is " + str(remaining_cap) + ".")
        print("Please return to the volunteer menu if the refugee's family is larger than this number.")

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
                gender = add_gender()
                if gender == 0:
                    return
                elif gender == 9:
                    progress -= 1
                else:
                    progress += 1

            elif progress == 2:
                date_of_birth = add_dob()
                if date_of_birth == "0":
                    return
                elif date_of_birth == "9":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 3:
                medical_cond = add_medical_cond()
                if medical_cond == 0:
                    return
                elif medical_cond == 9:
                    progress -= 1
                else:
                    progress += 1

            elif progress == 4:
                family = add_family()
                if family == "X":
                    return
                elif family == "B":
                    progress -= 1
                else:
                    progress += 1

            elif progress == 5:
                remarks = add_remarks()
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
                   'date_of_birth': [date_of_birth], 'camp_name': [self.camp_name], 'medical_condition': [medical_cond],
                   'family_members': [family], 'remarks': [remarks]}
        new = pd.DataFrame(new_row)
        refugees = pd.concat([refugees, new], ignore_index=True)
        refugees.to_csv('refugees.csv', index=False)

        camps = pd.read_csv('camps.csv')
        chosen = (camps['camp_name'] == self.camp_name)
        camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] + family
        camps.to_csv('camps.csv', index=False)

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
        if not self.camp_name:
            print("\nVolunteers can only view refugee profiles for their current camp. Please add your camp identification.")
            return

        print("\nView refugee profile")
        refugees = pd.read_csv('refugees.csv')
        refugees = refugees[refugees['camp_name'] == self.camp_name]
        if len(refugees.index) == 0:
            print("There are no refugees at your current camp.")
            return

        refugees = refugees.replace({np.nan: None})
        print("You will be prompted for the refugee ID of the refugee whose profile you would like to view.")
        while True:
            print("Enter [1] to proceed")
            print("Enter [2] to list all refugees at your current camp")
            print("Enter [0] to return to the volunteer menu")
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
            print("\nEnter [0] to return to the volunteer menu.")
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
        print("Date of birth:", date_of_birth)
        print("Medical condition:", medical_str)
        print("No. of family members:", family)
        print("Additional remarks:", remarks)
        return

    def edit_refugee_profile(self):
        def edit_refugee_name(refugee_id, refugee_name):
            print("\nRefugee's current name is:", refugee_name)
            while True:
                print("Enter [0] to return to the previous step.")
                new_name = input("Enter refugee's new name: ").strip()
                if new_name == "0":
                    return
                if new_name == refugee_name:
                    print("New name is the same as current name. Please enter a different name.")
                    continue
                if new_name == "":
                    print("Please enter a name.")
                    continue
                s = re.search("^[A-Z][a-zA-Z-' ]*$", refugee_name)
                if not s:
                    print("Name can only contain letters, hyphen (-) and apostrophe ('), and must start with a capital letter.")
                    continue
                break
            # update csv file
            refugees = pd.read_csv('refugees.csv')
            cur = (refugees['refugee_id'] == refugee_id)
            refugees.loc[cur, 'refugee_name'] = new_name
            refugees.to_csv('refugees.csv', index=False)
            print("Refugee's name has been changed to:", new_name)
            return

        def edit_gender(refugee_id, gender):
            gender_str = convert_gender(gender)

            print("\nRefugee's current gender is:", gender_str)
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
                if new_gender == gender:
                    print("New gender is the same as current gender. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            refugees = pd.read_csv('refugees.csv')
            cur = (refugees['refugee_id'] == refugee_id)
            refugees.loc[cur, 'gender'] = new_gender
            refugees.to_csv('refugees.csv', index=False)
            new_gender_str = convert_gender(new_gender)
            print("Refugee's gender has been changed to:", new_gender_str)
            return

        def edit_medical_cond(refugee_id, medical_cond):
            medical_str = convert_medical_condition(medical_cond)

            print("\nRefugee's current medical condition is:", medical_str)
            while True:
                print("Enter [0] to return to the previous step.")
                print("New medical condition:")
                print("Enter [1] for Healthy")
                print("Enter [2] for Minor illness with no injuries")
                print("Enter [3] for Major illness with no injuries")
                print("Enter [4] for Minor injury with no illness")
                print("Enter [5] for Major injury with no illness")
                print("Enter [6] for Illness and injury (non-critical)")
                print("Enter [7] for Critical condition (illness and/or injury)")
                try:
                    new_medical_cond = int(input("Select an option: "))
                    if new_medical_cond not in range(8):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                if new_medical_cond == 0:
                    return
                if new_medical_cond == medical_cond:
                    print("Medical condition is unchanged. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            refugees = pd.read_csv('refugees.csv')
            cur = (refugees['refugee_id'] == refugee_id)
            refugees.loc[cur, 'medical_condition'] = new_medical_cond
            refugees.to_csv('refugees.csv', index=False)
            new_medical_str = convert_medical_condition(new_medical_cond)
            print("Refugee's medical condition has been changed to:", new_medical_str)
            return

        def edit_family(refugee_id, family):
            print("\nCurrent no. of members in refugee's family:", family)
            camps = pd.read_csv('camps.csv')
            cur_camp = camps[camps['camp_name'] == self.camp_name]
            remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']
            print("Your camp's remaining capacity is " + str(remaining_cap) + ".")
            print("Please return to the previous step if the update would cause the camp's capacity to be exceeded.")

            while True:
                print("\nEnter [X] to return to the previous step.")
                new_family = input("New number of family members: ")
                if new_family == "X":
                    return
                try:
                    new_family = int(new_family)
                    if new_family < 1:
                        raise ValueError
                except ValueError:
                    print("Please enter a positive integer.")
                    continue
                if new_family-family > remaining_cap:
                    print("Addition of family members causes camp's capacity to be exceeded. Please re-enter or return to the previous step.")
                    continue
                if new_family == family:
                    print("Number of family members is unchanged. Please try again or return to the previous step.")
                    continue
                if new_family > 12:
                    while True:
                        print("\nWarning: Refugee's family has more than 12 members based on input.")
                        print("Do you wish to proceed?")
                        print("Enter [1] to proceed")
                        print("Enter [9] to re-enter number of family members")
                        try:
                            largefam_option = int(input("Select an option: "))
                            if largefam_option not in (1, 9):
                                raise ValueError
                        except ValueError:
                            print("Please enter a number from the options provided.")
                            continue
                        break
                    if largefam_option == "9":
                        continue
                break
            # update csv files
            refugees = pd.read_csv('refugees.csv')
            cur = (refugees['refugee_id'] == refugee_id)
            refugees.loc[cur, 'family_members'] = new_family
            refugees.to_csv('refugees.csv', index=False)
            print("New no. of members in refugee's family:", new_family)

            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] - family + new_family
            camps.to_csv('camps.csv', index=False)
            return

        def edit_remarks(refugee_id, remarks):
            print("\nCurrent remarks on refugee:", remarks)
            while True:
                print("Enter [0] to return to the previous step.")
                try:
                    new_remarks = input("Enter updated remarks (optional, max 200 characters): ").strip()
                    if new_remarks == "0":
                        return
                    s = re.search("[a-zA-Z]", new_remarks)
                    if new_remarks != "" and not s:
                        raise ValueError
                except ValueError:
                    print("Please ensure remarks contain text.")
                    continue
                if len(new_remarks) > 200:
                    print("Remarks cannot exceed 200 characters.")
                    continue
                if new_remarks == remarks or (not new_remarks and not remarks):
                    print("Remarks are unchanged. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            refugees = pd.read_csv('refugees.csv')
            cur = (refugees['refugee_id'] == refugee_id)
            refugees.loc[cur, 'remarks'] = new_remarks
            refugees.to_csv('refugees.csv', index=False)
            print("Remarks on refugee have been changed to:", new_remarks)
            return

        def remove_refugee(refugee_id, refugee_name, family):
            print("\nAre you sure you would like to remove the profile of " + refugee_name + "?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the volunteer menu")
            while True:
                try:
                    remove_option = int(input("Select an option: "))
                    if remove_option not in (0, 1):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.\n")
                    continue
                break
            if remove_option == 0:
                return

            # update csv files
            refugees = pd.read_csv('refugees.csv')
            refugees = refugees.drop(refugees[refugees['refugee_id'] == refugee_id].index)
            refugees.to_csv('refugees.csv', index=False)

            camps = pd.read_csv('camps.csv')
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] - family
            camps.to_csv('camps.csv', index=False)

            print("Refugee's profile has been removed.")
            return

        if not self.camp_name:
            print("\nVolunteers can only edit refugee profiles for their current camp. Please add your camp identification.")
            return

        print("\nEdit or remove refugee profile")
        refugees = pd.read_csv('refugees.csv')
        refugees = refugees[refugees['camp_name'] == self.camp_name]
        if len(refugees.index) == 0:
            print("There are no refugees at your current camp.")
            return

        refugees = refugees.replace({np.nan: None})
        print("You will be prompted for the refugee ID of the refugee whose profile you would like to edit.")
        while True:
            print("Enter [1] to proceed")
            print("Enter [2] to list all refugees at your current camp")
            print("Enter [0] to return to the volunteer menu")
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
            print("\nEnter [0] to return to the volunteer menu.")
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
                print("Enter [0] to return to the volunteer menu")
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
                edit_refugee_name(refugee_id, refugee_name)
            if option == 2:
                edit_gender(refugee_id, gender)
            if option == 3:
                edit_medical_cond(refugee_id, medical_cond)
            if option == 4:
                edit_family(refugee_id, family)
            if option == 5:
                edit_remarks(refugee_id, remarks)
            if option == 9:
                remove_refugee(refugee_id, refugee_name, family)
                return

    def display_camp_info(self):
        print("\nDisplay camp information")
        if not self.camp_name:
            print("You currently do not belong to a camp. Please add your camp identification.")
            return

        camps = pd.read_csv("camps.csv")
        my_camp = camps[camps['camp_name'] == self.camp_name]
        print("Your camp is " + self.camp_name + ", supporting " + my_camp.iloc[0]['plan_name'] + ".")
        print("Number of volunteers: ", my_camp.iloc[0]['volunteers'])
        print("Number of refugees: ", my_camp.iloc[0]['refugees'])
        print("Refugee capacity: ", my_camp.iloc[0]['capacity'])
        print("\nResources available")
        print("Food packets:", my_camp.iloc[0]['food'])
        print("Water portions:", my_camp.iloc[0]['water'])
        print("Medical kits:", my_camp.iloc[0]['medical_supplies'])
        return

    def update_camp_info(self):
        def edit_capacity():
            camps = pd.read_csv("camps.csv")
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
            camps.to_csv('camps.csv', index=False)
            print("New refugee capacity:", new_capacity)
            return

        def edit_food():
            camps = pd.read_csv("camps.csv")
            my_camp = camps[camps['camp_name'] == self.camp_name]
            print("\nCurrent supply of food packets at " + self.camp_name + ": " + str(my_camp.iloc[0]['food']))

            while True:
                print("\nEnter [X] to return to the previous step.")
                new_food = input("Updated supply of food packets: ")
                if new_food == "X":
                    return
                try:
                    new_food = int(new_food)
                    if new_food < 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a non-negative integer.")
                    continue
                if new_food == my_camp.iloc[0]['food']:
                    print("Food supply is unchanged. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'food'] = new_food
            camps.to_csv('camps.csv', index=False)
            print("Updated supply of food packets:", new_food)
            return

        def edit_water():
            camps = pd.read_csv("camps.csv")
            my_camp = camps[camps['camp_name'] == self.camp_name]
            print("\nCurrent supply of water portions at " + self.camp_name + ": " + str(my_camp.iloc[0]['water']))

            while True:
                print("\nEnter [X] to return to the previous step.")
                new_water = input("Updated supply of water portions: ")
                if new_water == "X":
                    return
                try:
                    new_water = int(new_water)
                    if new_water < 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a non-negative integer.")
                    continue
                if new_water == my_camp.iloc[0]['water']:
                    print("Water supply is unchanged. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'water'] = new_water
            camps.to_csv('camps.csv', index=False)
            print("Updated supply of water portions:", new_water)
            return

        def edit_medical_supplies():
            camps = pd.read_csv("camps.csv")
            my_camp = camps[camps['camp_name'] == self.camp_name]
            print("\nCurrent supply of medical kits at " + self.camp_name + ": " + str(my_camp.iloc[0]['medical_supplies']))

            while True:
                print("\nEnter [X] to return to the previous step.")
                new_medical = input("Updated supply of medical kits: ")
                if new_medical == "X":
                    return
                try:
                    new_medical = int(new_medical)
                    if new_medical < 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a non-negative integer.")
                    continue
                if new_medical == my_camp.iloc[0]['medical_supplies']:
                    print("Medical supplies are unchanged. Please try again or return to the previous step.")
                    continue
                break
            # update csv file
            chosen = (camps['camp_name'] == self.camp_name)
            camps.loc[chosen, 'medical_supplies'] = new_medical
            camps.to_csv('camps.csv', index=False)
            print("Updated supply of medical kits:", new_medical)
            return

        print("\nUpdate camp information")
        if not self.camp_name:
            print("You currently do not belong to a camp. Please add your camp identification.")
            return

        # outer loop to edit multiple attributes, exit if 0 is entered
        while True:
            # inner loop to catch invalid input
            while True:
                print("\nWhich details would you like to update?")
                print("Enter [1] for refugee capacity")
                print("Enter [2] for food packets")
                print("Enter [3] for water portions")
                print("Enter [4] for medical kits")
                print("Enter [0] to return to the volunteer menu")
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
