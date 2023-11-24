import re, datetime, pandas as pd
from coded_vars import convert_gender, convert_medical_condition

def add_name():
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        refugee_name = input("Enter refugee name: ").strip()
        if refugee_name in ("0", "9"):
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
        date_of_birth = input("Enter refugee's date of birth in the format DD-MM-YYYY: ").strip()
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
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
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


def add_family(remaining_cap):
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
        family = input("Number of family members: ")
        if family.upper() in ("X", "B"):
            return family.upper()
        try:
            family = int(family)
            if family < 1:
                raise ValueError
        except ValueError:
            print("Please enter a positive integer.")
            continue
        if family > remaining_cap:
            print("Number of family members exceeds camp's capacity. Please re-enter or return to the previous menu.")
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
            if largefam_option == 9:
                continue
        return family


def add_remarks():
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
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

def edit_refugee_name(refugee_id, refugee_name):
    print("\nRefugee's current name is:", refugee_name)
    while True:
        print("Enter [0] to return to the previous step.")
        new_name = input("Enter refugee's new name: ").strip()
        if new_name == "0":
            return
        elif new_name == refugee_name:
            print("New name is the same as current name. Please enter a different name.")
            continue
        else:
            new_name = f"{new_name[0].upper()}{new_name[1:]}"
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

def edit_dob(refugee_id, date_of_birth):
    print("\nRefugee's current date of birth (DD-MM-YYYY) is:", date_of_birth)
    while True:
        print("Enter [0] to return to the previous step.")
        new_dob = input("Enter refugee's corrected date of birth: ").strip()
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
        if t.year - ndob.year > 121 or (t.year - ndob.year == 121 and t.month > ndob.month) or (
                t.year - ndob.year == 121 and t.month == ndob.month and t.day >= ndob.day):
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
        break
    # update csv file
    refugees = pd.read_csv('refugees.csv')
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'date_of_birth'] = new_dob
    refugees.to_csv('refugees.csv', index=False)
    print("Refugee's date of birth has been changed to:", new_dob)
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

def edit_family(plan_id, camp_name, refugee_id, family):
    print("\nCurrent no. of members in refugee's family:", family)
    camps = pd.read_csv(plan_id + '.csv')
    cur_camp = camps[camps['camp_name'] == camp_name]
    remaining_cap = cur_camp.iloc[0]['capacity'] - cur_camp.iloc[0]['refugees']
    print("Your camp's remaining capacity is " + str(remaining_cap) + ".")
    print("Please return to the previous step if the update would cause the camp's capacity to be exceeded.")

    while True:
        print("\nEnter [X] to return to the previous step.")
        new_family = input("New number of family members: ")
        if new_family.upper() == "X":
            return
        try:
            new_family = int(new_family)
            if new_family < 1:
                raise ValueError
        except ValueError:
            print("Please enter a positive integer.")
            continue
        if new_family - family > remaining_cap:
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
            if largefam_option == 9:
                continue
        break
    # update csv files
    refugees = pd.read_csv('refugees.csv')
    cur = (refugees['refugee_id'] == refugee_id)
    refugees.loc[cur, 'family_members'] = new_family
    refugees.to_csv('refugees.csv', index=False)
    print("New no. of members in refugee's family:", new_family)

    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] - family + new_family
    camps.to_csv(plan_id + '.csv', index=False)
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

def remove_refugee(plan_id, camp_name, refugee_id, refugee_name, family):
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
            continue
        break
    if remove_option == 0:
        return

    # update csv files
    refugees = pd.read_csv('refugees.csv')
    refugees = refugees.drop(refugees[refugees['refugee_id'] == refugee_id].index)
    refugees.to_csv('refugees.csv', index=False)

    camps = pd.read_csv(plan_id + '.csv')
    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'refugees'] = camps.loc[chosen, 'refugees'] - family
    camps.to_csv(plan_id + '.csv', index=False)

    print("Refugee's profile has been removed.")
    return