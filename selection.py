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

# select plan allowing user to go back to direct username vs plan->camp->volunteer
def select_plan2():
    print("\nSelect a humanitarian plan.")
    plans = pd.read_csv('humanitarian_plan.csv')
    plans = plans[plans['end_date'].isna()]
    print("Number - Location - Start Date")
    for row in range(len(plans.index)):
        print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], sep=" - ")

    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
        plan_num = input("Enter the number of your chosen plan: ")
        if plan_num in ("X", "B"):
            return plan_num
        try:
            plan_num = int(plan_num)
            if plan_num not in range(1, len(plans.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a plan number corresponding to a humanitarian plan listed above.")
            continue
        return plans['plan_id'].iloc[plan_num-1]

# select camp allowing user to go back to plan selection
def select_camp(plan_id):
    print("\nSelect a camp.")
    camps = pd.read_csv(plan_id + ".csv")
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to plan selection.")
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

# same as above, but includes volunteers with no camp identification
def select_camp_none(plan_id):
    print("\nSelect a camp.")
    camps = pd.read_csv(plan_id + ".csv")
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to plan selection.")
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

# active = 1 means only active volunteers can be selected
def select_volunteer(plan_id, camp_name, active):
    users = pd.read_csv('users.csv', dtype={'password': str})
    if active:
        users = users[(users['account_type'] == "volunteer") & (users['active'] == 1)]
    else:
        users = users[users['account_type'] == "volunteer"]
    users = users.replace({np.nan: None})
    if camp_name:
        users = users[(users['plan_id'] == plan_id) & (users['camp_name'] == camp_name)]
    else:
        users = users[(users['plan_id'] == plan_id) & (users['camp_name'].isna())]
    if len(users.index) == 0:
        if active:
            print("There are no active volunteers at the selected camp. Please try again.")
        else:
            print("There are no volunteers at the selected camp. Please try again.")
        return "9"

    print("\nSelect a volunteer.")
    while True:
        print("Enter [0] to return to the previous menu or [9] to go back to camp selection.")
        if active:
            print("Enter [1] to list the usernames of all active volunteers at the selected camp.")
        else:
            print("Enter [1] to list the usernames of all volunteers at the selected camp.")
        username = input("Enter the username of your chosen volunteer: ")
        if username in ("0", "9"):
            return username
        if username == "1":
            if camp_name:
                print("Volunteers at plan", plan_id + ",", camp_name + ":")
            else:
                print("Volunteers at plan", plan_id, "with no camp identification:")

            if active:
                for row in range(len(users.index)):
                    print(users['username'].iloc[row])
            else:
                print("Username - Status")
                for row in range(len(users.index)):
                    if users['active'].iloc[row] == 1:
                        print(users['username'].iloc[row], "Active", sep=" - ")
                    else:
                        print(users['username'].iloc[row], "Deactivated", sep=" - ")
            print("")
            continue
        if username not in users['username'].values:
            print("Username not found. Please enter again.\n")
            continue
        return username

# allows user to choose whether to enter username directly or go through plan->camp->volunteer
def initial_selection(active):
    while True:
        users = pd.read_csv('users.csv', dtype={'password': str})
        if active:
            users = users[(users['account_type'] == "volunteer") & (users['active'] == 1)]
        else:
            users = users[users['account_type'] == "volunteer"]
        if len(users.index) == 0:
            if active:
                print("There are no active volunteer accounts.")
            else:
                print("There are no volunteer accounts.")
            return 0

        print("\nEnter [1] to select a volunteer by entering the username directly")
        print("Enter [2] to filter by plan and camp before selecting a volunteer")
        print("Enter [0] to return to the previous menu")
        try:
            option = int(input("Select an option: "))
            if option not in range(3):
                raise ValueError
        except:
            print("Please enter a number from the options provided.")
            continue
        if option in (0, 2):
            return option

        # select volunteer directly
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            username = input("Enter the username of your chosen volunteer: ")
            if username == "0":
                return 0
            if username == "9":
                break
            if username not in users['username'].values:
                print("Username not found. Please try again.")
                continue
            break

        if username == "9":
            continue
        select_user = users[users['username'] == username]
        return select_user.iloc[0]['plan_id'], select_user.iloc[0]['camp_name'], username

# for admin methods requiring volunteer to be selected at the start (but no further progress loop)
# returns 0 if user chooses to return to previous memu
def select_plan_camp_vol(active):
    progress = 0
    while progress < 4:
        if progress == 0:
            select_user = initial_selection(active)
            if select_user == 0:
                return 0
            elif select_user == 2:
                progress += 1
            else:
                return select_user

        if progress == 1:
            plan_id = select_plan2()
            if plan_id == "X":
                return 0
            elif plan_id == "B":
                progress -= 1
            else:
                progress += 1

        if progress == 2:
            camp_name = select_camp(plan_id)
            if camp_name == "X":
                return 0
            elif camp_name == "B":
                progress -= 1
            else:
                progress += 1

        if progress == 3:
            username = select_volunteer(plan_id, camp_name, active)
            if username == "0":
                return 0
            elif username == "9":
                progress -= 1
            else:
                progress += 1

    return plan_id, camp_name, username

# includes volunteers with no camp identification
def select_plan_camp_vol_none(active):
    progress = 0
    while progress < 4:
        if progress == 0:
            select_user = initial_selection(active)
            if select_user == 0:
                return 0
            elif select_user == 2:
                progress += 1
            else:
                return select_user

        if progress == 1:
            plan_id = select_plan2()
            if plan_id == "X":
                return 0
            elif plan_id == "B":
                progress -= 1
            else:
                progress += 1

        if progress == 2:
            camp_name = select_camp_none(plan_id)
            if camp_name == "X":
                return 0
            elif camp_name == "B":
                progress -= 1
            else:
                progress += 1

        if progress == 3:
            username = select_volunteer(plan_id, camp_name, active)
            if username == "0":
                return 0
            elif username == "9":
                progress -= 1
            else:
                progress += 1

    return plan_id, camp_name, username