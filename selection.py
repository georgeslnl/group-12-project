import pandas as pd, numpy as np

def select_plan():
    print("\nSelect a humanitarian plan.")
    plans = pd.read_csv('humanitarian_plan.csv')
    plans = plans[plans['end_date'].isna()]
    print("Number - Location - Start Date")
    for row in range(len(plans.index)):
        print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], sep=" - ")

    while True:
        print("\nEnter [0] to return to the previous menu.")
        try:
            plan_num = int(input("Enter the number of your chosen plan: "))
            if plan_num == 0:
                return plan_num
            if plan_num not in range(1, len(plans.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a plan number corresponding to a humanitarian plan listed above.")
            continue
        return plans['plan_id'].iloc[plan_num-1]

def select_camp(plan_id):
    print("\nSelect a camp.")
    camps = pd.read_csv(plan_id + ".csv")
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    while True:
        print("\nEnter [0] to return to the previous menu.")
        try:
            camp_num = int(input("Enter the number of your chosen camp: "))
            if camp_num == 0:
                return camp_num
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a camp number corresponding to a camp listed above.")
            continue
        return camps['camp_name'].iloc[camp_num-1]

# select camp allowing user to go back to plan selection
def select_camp2(plan_id):
    print("\nSelect a camp.")
    camps = pd.read_csv(plan_id + ".csv")
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
        camp_num = input("Enter the number of your chosen camp: ")
        if camp_num in ("X", "B"):
            return camp_num
        try:
            camp_num = int(camp_num)
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a camp number corresponding to a camp listed above.")
            continue
        return camps['camp_name'].iloc[camp_num-1]

# includes volunteers with no camp identification
def select_camp_none(plan_id):
    print("\nSelect a camp.")
    camps = pd.read_csv(plan_id + ".csv")
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
        print("If the volunteer has no camp identification, enter [0].")
        camp_num = input("Enter the number of your chosen camp: ")
        if camp_num in ("X", "B"):
            return camp_num
        if camp_num == "0":
            return None
        try:
            camp_num = int(camp_num)
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a camp number corresponding to a camp listed above.")
            continue
        return camps['camp_name'].iloc[camp_num-1]

def select_volunteer(plan_id, camp_name):
    users = pd.read_csv('users.csv', dtype={'password': str})
    users = users.replace({np.nan: None})
    if camp_name:
        users = users[(users['plan_id'] == plan_id) & (users['camp_name'] == camp_name)]
    else:
        users = users[(users['plan_id'] == plan_id) & (users['camp_name'].isna())]
    if len(users.index) == 0:
        print("There are no volunteers at the selected camp. Please try again.")
        return "9"

    print("\nSelect a volunteer.")
    while True:
        print("Enter [0] to return to the previous menu or [9] to go back to the previous step.")
        print("Enter [1] to list the usernames of all volunteers at the selected camp.")
        username = input("Enter the username of your chosen volunteer: ")
        if username in ("0", "9"):
            return username
        if username == "1":
            if camp_name:
                print("Volunteers at plan", plan_id + ",", camp_name + ":")
            else:
                print("Volunteers at plan", plan_id, "with no camp identification:")
            for row in range(len(users.index)):
                print(users['username'].iloc[row])
            print("")
            continue
        if username not in users['username'].values:
            print("Username not found. Please enter again.\n")
            continue
        return username


# for admin methods requiring plan, camp and volunteer to be selected at the start (but no further progress loop)
# returns 0 if user chooses to return to previous memu
def select_plan_camp_vol():
    progress = 0
    while progress < 3:
        if progress == 0:
            plan_id = select_plan()
            if plan_id == 0:
                return 0
            else:
                progress += 1

        if progress == 1:
            camp_name = select_camp2(plan_id)
            if camp_name == "X":
                return 0
            elif camp_name == "B":
                progress -= 1
            else:
                progress += 1

        if progress == 2:
            username = select_volunteer(plan_id, camp_name)
            if username == "0":
                return 0
            elif username == "9":
                progress -= 1
            else:
                progress += 1

    return plan_id, camp_name, username

# includes volunteers with no camp identification
def select_plan_camp_vol_none():
    progress = 0
    while progress < 3:
        if progress == 0:
            plan_id = select_plan()
            if plan_id == 0:
                return 0
            else:
                progress += 1

        if progress == 1:
            camp_name = select_camp_none(plan_id)
            if camp_name == "X":
                return 0
            elif camp_name == "B":
                progress -= 1
            else:
                progress += 1

        if progress == 2:
            username = select_volunteer(plan_id, camp_name)
            if username == "0":
                return 0
            elif username == "9":
                progress -= 1
            else:
                progress += 1

    return plan_id, camp_name, username