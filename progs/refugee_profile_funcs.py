import re, datetime, pandas as pd, os
import logging
from progs.coded_vars import convert_gender, convert_medical_condition

def add_name():
    """Prompts the user to enter the refugee's name."""
    logging.debug("User prompted to enter refugee name.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back one step.\n")
        refugee_name = input(">>Enter refugee's name: ").strip()
        if refugee_name in ("0", "9"):
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


def add_gender():
    """Prompts the user to select the refugee's gender."""
    logging.debug("User prompted to select gender.")
    while True:
        print("\nGender:")
        print("Enter [1] for male")
        print("Enter [2] for female")
        print("Enter [3] for non-binary")
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.\n")
        try:
            gender = int(input(">>Select an option: "))
            if gender not in (0, 1, 2, 3, 9):
                raise ValueError
        except ValueError:
            print("\nPlease enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        return gender


def add_dob():
    """
    Prompts the user to enter the refugee's date of birth.
    If the refugee is over 120 years old based on the input, a warning is displayed and the user is asked to confirm the input.
    """
    logging.debug("User prompted to enter date of birth.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back one step.\n")
        date_of_birth = input(">>Enter refugee's date of birth in the format DD-MM-YYYY: ").strip()
        if date_of_birth in ("0", "9"):
            return date_of_birth
        try:
            dob = datetime.datetime.strptime(date_of_birth, "%d-%m-%Y").date()
        except ValueError:
            print("\nIncorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
            logging.error("Invalid user input.")
            continue
        t = datetime.date.today()
        if dob > t:
            print("\nDate of birth cannot be in the future. Please try again.")
            logging.error("User entered a date of birth in the future.")
            continue
        if t.year - dob.year > 121 or (t.year - dob.year == 121 and t.month > dob.month) or (
                t.year - dob.year == 121 and t.month == dob.month and t.day >= dob.day):
            logging.warning("Refugee is over 120 years old based on date of birth.")
            logging.debug("User prompted to confirm date of birth.")
            while True:
                print("\nWarning: Refugee is over 120 years old based on date of birth.")
                print("Do you wish to proceed?")
                print("Enter [1] to proceed")
                print("Enter [9] to re-enter date of birth\n")
                try:
                    overage_option = int(input(">>Select an option: "))
                    if overage_option not in (1, 9):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                break
            if overage_option == 9:
                logging.debug("Returning to previous step.")
                continue
            logging.error("Date of birth confirmed.")
        return date_of_birth


def add_medical_cond():
    """Prompts the user to select the refugee's medical condition."""
    logging.debug("User prompted to select medical condition.")
    while True:
        print("\nMedical condition:")
        print("Enter [1] for Healthy")
        print("Enter [2] for Minor illness with no injuries")
        print("Enter [3] for Major illness with no injuries")
        print("Enter [4] for Minor injury with no illness")
        print("Enter [5] for Major injury with no illness")
        print("Enter [6] for Illness and injury (non-critical)")
        print("Enter [7] for Critical condition (illness and/or injury)")
        print("Enter [0] to return to the previous menu or [9] to go back one step.\n")

        try:
            medical_cond = int(input(">>Select an option: "))
            if medical_cond not in (0, 1, 2, 3, 4, 5, 6, 7, 9):
                raise ValueError
        except ValueError:
            print("\nPlease enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        return medical_cond


def add_family(remaining_cap):
    """
    Prompts the user to enter the refugee's family size.
    If the family size exceeds 12, a warning is displayed and the user is asked to confirm the input.
    """
    logging.debug("User prompted to enter number of family members.")
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back one step.\n")
        family = input(">>Number of family members: ")
        if family.upper() in ("X", "B"):
            return family.upper()
        try:
            family = int(family)
            if family < 1:
                raise ValueError
        except ValueError:
            print("\nPlease enter a positive integer.")
            logging.error("Invalid user input.")
            continue
        if family > remaining_cap:
            print("\nNumber of family members exceeds camp's capacity. Please re-enter or return to the previous menu.")
            logging.error("Camp has insufficient capacity for the number of family members entered.")
            continue
        if family > 12:
            logging.warning("Number of family members entered is more than 12.")
            logging.debug("User prompted to confirm number of family members.")
            while True:
                print("\nWarning: Refugee's family has more than 12 members based on input.")
                print("Do you wish to proceed?")
                print("Enter [1] to proceed")
                print("Enter [9] to re-enter number of family members\n")
                try:
                    largefam_option = int(input(">>Select an option: "))
                    if largefam_option not in (1, 9):
                        raise ValueError
                except ValueError:
                    print("\nPlease enter a number from the options provided.")
                    continue
                break
            if largefam_option == 9:
                logging.debug("Returning to previous step.")
                continue
            logging.debug("Number of family members confirmed.")
        return family


def add_remarks():
    """Prompts the user to enter any additional remarks on the refugee."""
    logging.debug("User prompted to enter optional remarks.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back one step.\n")
        try:
            remarks = input(">>Enter additional remarks (optional, max 200 characters): ").strip()
            if remarks in ("0", "9"):
                return remarks
            s = re.search("[a-zA-Z]", remarks)
            if remarks != "" and not s:
                raise ValueError
        except ValueError:
            print("\nPlease ensure remarks contain text.")
            logging.error("Invalid user input.")
            continue
        if len(remarks) > 200:
            print("\nRemarks cannot exceed 200 characters.")
            logging.error("Remarks entered are too long.")
            continue
        return remarks


def edit_refugee_name(refugee_id, refugee_name):
    """Prompts the user to enter the refugee's new name."""
    logging.debug("User prompted to enter new refugee name.")
    print("\nRefugee's current name is:", refugee_name)
    while True:
        print("Enter [0] to return to the previous step.")
        new_name = input("Enter refugee's new name: ").strip()
        if new_name == "0":
            logging.debug("Returning to previous step.")
            return
        elif new_name == refugee_name:
            print("New name is the same as current name. Please enter a different name.")
            logging.error("Refugee name is unchanged.")
            continue
        else:
            new_name = f"{new_name[0].upper()}{new_name[1:]}"
            break
    # update csv file
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'refugee_name'] = new_name
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")
    print("Refugee's name has been changed to:", new_name)
    logging.debug("Refugee name updated successfully")
    return

def edit_gender(refugee_id, gender):
    """Prompts the user to select the refugee's new gender."""
    gender_str = convert_gender(gender)
    print("\nRefugee's current gender is:", gender_str)
    logging.debug("User prompted to select new gender.")
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
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'gender'] = new_gender
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")
    new_gender_str = convert_gender(new_gender)
    print("Refugee's gender has been changed to:", new_gender_str)
    logging.debug("Gender updated successfully")
    return

def edit_dob(refugee_id, date_of_birth):
    """
    Prompts the user to enter the refugee's corrected date of birth.
    If the refugee is over 120 years old based on the input, a warning is displayed and the user is asked to confirm the input.
    """
    print("\nRefugee's current date of birth (DD-MM-YYYY) is:", date_of_birth)
    logging.debug("User prompted to enter corrected date of birth.")
    while True:
        print("Enter [0] to return to the previous step.")
        new_dob = input("Enter refugee's corrected date of birth: ").strip()
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
            logging.error("User entered a date of birth in the future.")
            continue
        if t.year - ndob.year > 121 or (t.year - ndob.year == 121 and t.month > ndob.month) or (
                t.year - ndob.year == 121 and t.month == ndob.month and t.day >= ndob.day):
            logging.warning("Refugee is over 120 years old based on date of birth.")
            logging.debug("User prompted to confirm date of birth.")
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
                    logging.error("Invalid user input.")
                    continue
                break
            if overage_option == 9:
                logging.debug("Returning to previous step.")
                continue
            logging.debug("Date of birth confirmed.")
        break
    # update csv file
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'date_of_birth'] = new_dob
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")
    print("Refugee's date of birth has been changed to:", new_dob)
    logging.debug("Date of birth updated successfully")
    return

def edit_medical_cond(refugee_id, medical_cond):
    """Prompts the user to select the refugee's new medical condition."""
    medical_str = convert_medical_condition(medical_cond)
    print("\nRefugee's current medical condition is:", medical_str)
    logging.debug("User prompted to select new medical condition.")
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
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        if new_medical_cond == 0:
            logging.debug("Returning to previous step.")
            return
        if new_medical_cond == medical_cond:
            print("Medical condition is unchanged. Please try again or return to the previous step.")
            logging.error("Medical condition is unchanged.")
            continue
        break
    # update csv file
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'medical_condition'] = new_medical_cond
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")
    new_medical_str = convert_medical_condition(new_medical_cond)
    print("Refugee's medical condition has been changed to:", new_medical_str)
    logging.debug("Medical condition updated successfully")
    return

def edit_family(plan_id, camp_name, refugee_id, family):
    """
    Prompts the user to enter the refugee's new family size.
    If the family size exceeds 12, a warning is displayed and the user is asked to confirm the input.
    """
    print("\nCurrent no. of members in refugee's family:", family)
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    cur_camp = camps[camps['camp_name'] == camp_name]
    remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']
    print("Your camp's remaining capacity is " + str(remaining_cap) + ".")
    print("Please return to the previous step if the update would cause the camp's capacity to be exceeded.")

    logging.debug("User prompted to enter new family size.")
    while True:
        print("\nEnter [X] to return to the previous step.")
        new_family = input("New number of family members: ")
        if new_family.upper() == "X":
            logging.debug("Returning to previous step.")
            return
        try:
            new_family = int(new_family)
            if new_family < 1:
                raise ValueError
        except ValueError:
            print("Please enter a positive integer.")
            logging.error("Invalid user input.")
            continue
        if new_family - family > remaining_cap:
            print("Addition of family members causes camp's capacity to be exceeded. Please re-enter or return to the previous step.")
            logging.error("Camp has insufficient capacity for the number of family members entered.")
            continue
        if new_family == family:
            print("Number of family members is unchanged. Please try again or return to the previous step.")
            logging.error("Family size is unchanged.")
            continue
        if new_family > 12:
            logging.warning("Number of family members entered is more than 12.")
            logging.debug("User prompted to confirm number of family members.")
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
                    logging.error("Invalid user input.")
                    continue
                break
            if largefam_option == 9:
                logging.debug("Returning to previous step.")
                continue
            logging.debug("Number of family members confirmed.")
        break
    # update csv files
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'family_members'] = new_family
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")
    print("New no. of members in refugee's family:", new_family)

    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] - family + new_family
    camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
    logging.debug("camps csv file updated")
    logging.debug("Family size updated successfully")
    return

def edit_remarks(refugee_id, remarks):
    """Prompts the user to enter the updated remarks on the refugee."""
    print("\nCurrent remarks on refugee:", remarks)
    logging.debug("User prompted to enter new remarks.")
    while True:
        print("Enter [0] to return to the previous step.")
        try:
            new_remarks = input("Enter updated remarks (optional, max 200 characters): ").strip()
            if new_remarks == "0":
                logging.debug("Returning to previous step.")
                return
            s = re.search("[a-zA-Z]", new_remarks)
            if new_remarks != "" and not s:
                raise ValueError
        except ValueError:
            print("Please ensure remarks contain text.")
            logging.error("Invalid user input.")
            continue
        if len(new_remarks) > 200:
            print("Remarks cannot exceed 200 characters.")
            logging.error("Remarks entered are too long.")
            continue
        if new_remarks == remarks or (not new_remarks and not remarks):
            print("Remarks are unchanged. Please try again or return to the previous step.")
            logging.error("Remarks are unchanged.")
            continue
        break
    # update csv file
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'remarks'] = new_remarks
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")
    print("Remarks on refugee have been changed to:", new_remarks)
    logging.debug("Remarks updated successfully")
    return

def remove_refugee(plan_id, camp_name, refugee_id, refugee_name, family):
    """Prompts the user to confirm that they wish to remove the profile of the selected refugee."""
    logging.debug(f"User prompted to confirm removal of refugee ID {refugee_id}.")
    while True:
        print("\nAre you sure you would like to remove the profile of " + refugee_name + "?")
        print("Enter [1] to proceed")
        print("Enter [0] to return to the previous menu")
        try:
            remove_option = int(input("Select an option: "))
            if remove_option not in (0, 1):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        break
    if remove_option == 0:
        logging.debug("Returning to previous menu.")
        return

    logging.debug("Removal of refugee profile confirmed.")
    # update csv files
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    refugees = refugees.drop(refugees[refugees['refugee_id'] == refugee_id].index)
    refugees.to_csv(os.path.join('data', 'refugees.csv'), index=False)
    logging.debug("refugees.csv updated")

    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] - family
    camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
    logging.debug("camps csv file updated")

    print("Refugee's profile has been removed.")
    logging.debug(f"Refugee ID {refugee_id} has been removed.")
    return
