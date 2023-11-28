import pandas as pd, numpy as np, os
import logging

# select plan allowing user to go back to direct username vs plan->camp->volunteer
def select_plan():
    """Prompts the admin to select a humanitarian plan."""
    print("\nSelect a humanitarian plan.")
    plans = pd.read_csv(os.path.join('data', 'humanitarian_plan.csv'))
    plans = plans[plans['end_date'].isna()]
    print("Number - Location - Start Date")
    for row in range(len(plans.index)):
        print(row + 1, plans['location'].iloc[row], plans['start_date'].iloc[row], sep=" - ")

    logging.debug("Admin prompted to select humanitarian plan.")
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
        plan_num = input(">>Enter the number of your chosen plan: ")
        if plan_num.upper() in ("X", "B"):
            return plan_num.upper()
        try:
            plan_num = int(plan_num)
            if plan_num not in range(1, len(plans.index) + 1):
                raise ValueError
        except ValueError:
            print("\nPlease enter a plan number corresponding to a humanitarian plan listed above.")
            logging.error("Invalid user input.")
            continue
        return plans['plan_id'].iloc[plan_num-1]

# select camp allowing user to go back to plan selection
def select_camp(plan_id, active):
    """
    Takes as input the plan_id of a humanitarian plan.
    Prompts the admin to select a camp at this plan.
    The function checks whether any volunteers can be selected at this plan and returns the admin to the previous step if not,
    noting that volunteers must have a camp to be selected.
    The parameter active (1 or 0) specifies whether the volunteer's account must be active to be selected.
    """
    users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
    if active:
        users = users[(users['account_type'] == "volunteer") & (users['plan_id'] == plan_id) & (users['active'] == 1)
                      & (users['camp_name'].notna())]
    else:
        users = users[(users['account_type'] == "volunteer") & (users['plan_id'] == plan_id)
                      & (users['camp_name'].notna())]
    if len(users.index) == 0:
        logging.warning("No volunteers to select from.")
        if active:
            print("\nThere are no camps with active volunteers at the selected plan. Please try again.")
        else:
            print("\nThere are no camps with volunteers at the selected plan. Please try again.")
        return "B"

    print("\nSelect a camp.")
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    logging.debug("Admin prompted to select camp.")
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to plan selection.")
        camp_num = input(">>Enter the number of your chosen camp: ")
        if camp_num.upper() in ("X", "B"):
            return camp_num.upper()
        try:
            camp_num = int(camp_num)
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("\nPlease enter a camp number corresponding to a camp listed above.")
            logging.error("Invalid user input.")
            continue
        return camps['camp_name'].iloc[camp_num-1]

# same as above, but includes volunteers with no camp identification
def select_camp_none(plan_id, active):
    """
    Takes as input the plan_id of a humanitarian plan.
    Prompts the admin to select a camp at this plan.
    The function checks whether any volunteers can be selected at this plan and returns the admin to the previous step if not.
    The parameter active (1 or 0) specifies whether the volunteer's account must be active to be selected.
    """
    users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
    if active:
        users = users[(users['account_type'] == "volunteer") & (users['plan_id'] == plan_id) & (users['active'] == 1)]
    else:
        users = users[(users['account_type'] == "volunteer") & (users['plan_id'] == plan_id)]
    if len(users.index) == 0:
        logging.warning("No volunteers to select from.")
        if active:
            print("\nThere are no active volunteers at the selected plan. Please try again.")
        else:
            print("\nThere are no volunteers at the selected plan. Please try again.")
        return "B"

    print("\nSelect a camp.")
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity",
              sep=" - ")

    logging.debug("Admin prompted to select camp.")
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to plan selection.")
        print("If the volunteer has no camp identification, enter [N].")
        camp_num = input(">>Enter the number of your chosen camp: ")
        if camp_num.upper() in ("X", "B"):
            return camp_num.upper()
        if camp_num.upper() == "N":
            return None
        try:
            camp_num = int(camp_num)
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("\nPlease enter a camp number corresponding to a camp listed above.")
            logging.error("Invalid user input.")
            continue
        return camps['camp_name'].iloc[camp_num-1]

# active = 1 means only active volunteers can be selected
def select_volunteer(plan_id, camp_name, active):
    """
    Takes as input the plan_id of a humanitarian plan and the name of a camp at this plan (which can be None).
    Prompts the admin to select a volunteer at this camp.
    The function checks whether any volunteers can be selected at this camp and returns the admin to the previous step if not.
    The admin is given the option to list all volunteers at the camp before entering the username.
    The parameter active (1 or 0) specifies whether the volunteer's account must be active to be selected.
    """
    users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
    users = users[(users['account_type'] == "volunteer") & (users['plan_id'] == plan_id)]
    users = users.replace({np.nan: None})
    if active:
        users = users[users['active'] == 1]
    if camp_name:
        users = users[users['camp_name'] == camp_name]
    else:
        users = users[users['camp_name'].isna()]
    if len(users.index) == 0:
        logging.warning("No volunteers to select from.")
        if active and camp_name:
            print("There are no active volunteers at the selected camp. Please try again.")
        elif active and not camp_name:
            print("There are no active volunteers with no camp identification. Please try again.")
        elif not active and camp_name:
            print("There are no volunteers at the selected camp. Please try again.")
        else:
            print("There are no volunteers with no camp identification. Please try again.")
        return "9"

    print("\nSelect a volunteer.")
    logging.debug("Admin prompted to enter volunteer's username.")
    while True:
        print("Enter [0] to return to the previous menu or [9] to go back to camp selection.")
        if active:
            print("Enter [1] to list the usernames of all active volunteers at the selected camp.")
        else:
            print("Enter [1] to list the usernames of all volunteers at the selected camp.")
        username = input(">>Enter the username of your chosen volunteer: ")
        if username in ("0", "9"):
            return username
        if username == "1":
            logging.debug("Admin selected to view all volunteers at selected camp.")
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
            logging.error("Username not found.")
            continue
        return username

# allows user to choose whether to enter username directly or go through plan->camp->volunteer
def initial_selection(active, none):
    """
    Prompts the admin to choose whether to select a volunteer by entering the username directly or selecting a humanitarian plan and camp first.
    If the admin chooses to enter the username directly, they are prompted for it.
    The function checks whether there are any volunteers that can be selected and returns the admin to the previous menu if not.
    The parameter active (1 or 0) specifies whether the volunteer's account must be active to be selected.
    The parameter none (1 or 0) specifies whether the volunteer must have a camp to be selected (none = 1 means volunteer need not have a camp).
    """
    while True:
        users = pd.read_csv(os.path.join('data', 'users.csv'), dtype={'password': str})
        users = users[users['account_type'] == "volunteer"]
        if active:
            users = users[users['active'] == 1]
        if not none:
            users = users[users['camp_name'].notna()]
        else:
            users = users[users['account_type'] == "volunteer"]
        if len(users.index) == 0:
            logging.warning("No volunteers to select from.")
            if active and none:
                print("There are no active volunteer accounts.")
            elif active and not none:
                print("There are no camps with active volunteer accounts.")
            elif not active and none:
                print("There are no volunteer accounts.")
            else: # not active and not none
                print("There are no camps with volunteer accounts.")
            return 0

        logging.debug("Admin prompted to choose between entering username directly and selecting plan and camp first.")
        print("\nEnter [1] to select a volunteer by entering the username directly")
        print("Enter [2] to filter by plan and camp before selecting a volunteer")
        print("Enter [0] to return to the previous menu\n")
        try:
            option = int(input(">>Select an option: "))
            if option not in range(3):
                raise ValueError
        except:
            print("\nPlease enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        if option in (0, 2):
            return option

        # select volunteer directly
        logging.debug("Admin prompted to enter volunteer's username.")
        while True:
            print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
            username = input(">>Enter the username of your chosen volunteer: ")
            if username == "0":
                return 0
            if username == "9":
                break
            if username not in users['username'].values:
                print("\nUsername not found. Please try again.")
                logging.error("Username not found.")
                continue
            break

        if username == "9":
            logging.debug("Returning to previous step.")
            continue
        select_user = users[users['username'] == username]
        return select_user.iloc[0]['plan_id'], select_user.iloc[0]['camp_name'], username

# for admin methods requiring volunteer to be selected at the start (but no further progress loop)
# returns 0 if user chooses to return to previous menu
# active is whether volunteer must be active to be selected
# none is whether volunteers with no camp identification can be selected
def select_plan_camp_vol(active, none):
    """
    Enables the admin to select a volunteer when using functionalities relating to volunteer accounts and volunteering sessions.
    The parameter active (1 or 0) specifies whether the volunteer's account must be active to be selected.
    The parameter none (1 or 0) specifies whether the volunteer must have a camp to be selected (none = 1 means volunteer need not have a camp).
    """
    progress = 0
    while progress < 4:
        if progress == 0:
            select_user = initial_selection(active, none)
            if select_user == 0:
                return 0
            elif select_user == 2:
                progress += 1
            else:
                return select_user

        if progress == 1:
            plan_id = select_plan()
            if plan_id == "X":
                return 0
            elif plan_id == "B":
                logging.debug("Returning to previous step.")
                progress -= 1
            else:
                progress += 1

        if progress == 2:
            if none:
                camp_name = select_camp_none(plan_id, active)
            else:
                camp_name = select_camp(plan_id, active)
            if camp_name == "X":
                return 0
            elif camp_name == "B":
                logging.debug("Returning to previous step.")
                progress -= 1
            else:
                progress += 1

        if progress == 3:
            username = select_volunteer(plan_id, camp_name, active)
            if username == "0":
                return 0
            elif username == "9":
                logging.debug("Returning to previous step.")
                progress -= 1
            else:
                progress += 1

    return plan_id, camp_name, username