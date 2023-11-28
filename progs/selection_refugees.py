import pandas as pd, os
import logging

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
        plan_num = input("Enter the number of your chosen plan: ")
        if plan_num.upper() in ("X", "B"):
            return plan_num.upper()
        try:
            plan_num = int(plan_num)
            if plan_num not in range(1, len(plans.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a plan number corresponding to a humanitarian plan listed above.")
            logging.error("Invalid user input.")
            continue
        return plans['plan_id'].iloc[plan_num-1]

# select camp allowing user to go back to plan selection
def select_camp(plan_id):
    """
    Takes as input the plan_id of a humanitarian plan.
    Prompts the admin to select a camp at this plan.
    The function checks whether any refugees can be selected at this plan and returns the admin to the previous step if not.
    """
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    refugees = refugees[refugees['plan_id'] == plan_id]
    if len(refugees.index) == 0:
        logging.warning("No refugees to select from.")
        print("There are no refugees at the selected plan. Please try again.")
        return "B"

    print("\nSelect a camp.")
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    print("Camp Name - # Volunteers - # Refugees - Refugee Capacity")
    for row in range(len(camps.index)):
        print(camps['camp_name'].iloc[row], str(camps['volunteers'].iloc[row]) + " volunteers",
              str(camps['refugees'].iloc[row]) + " refugees", str(camps['capacity'].iloc[row]) + " capacity", sep=" - ")

    logging.debug("Admin prompted to select camp.")
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to plan selection.")
        camp_num = input("Enter the number of your chosen camp: ")
        if camp_num.upper() in ("X", "B"):
            return camp_num.upper()
        try:
            camp_num = int(camp_num)
            if camp_num not in range(1, len(camps.index) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a camp number corresponding to a camp listed above.")
            logging.error("Invalid user input.")
            continue
        return camps['camp_name'].iloc[camp_num-1]

def select_refugee(plan_id, camp_name):
    """
    Takes as input the plan_id of a humanitarian plan and the name of a camp at this plan.
    Prompts the admin to select a refugee at this camp.
    The function checks whether any refugees can be selected at this camp and returns the admin to the previous step if not.
    The admin is given the option to list all refugees at the camp before entering the refugee ID.
    """
    refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
    refugees = refugees[(refugees['plan_id'] == plan_id) & (refugees['camp_name'] == camp_name)]
    if len(refugees.index) == 0:
        print("There are no refugees at the selected camp. Please try again.")
        return "B"

    print("\nSelect a refugee.")
    logging.debug("Admin prompted to enter refugee ID.")
    while True:
        print("Enter [X] to return to the previous menu or [B] to go back to camp selection.")
        print("Enter [S] to list all refugees at the selected camp.")
        refugee_id = input("Enter refugee ID: ")
        if refugee_id.upper() in ("X", "B"):
            return refugee_id.upper()
        if refugee_id.upper() == "S":
            logging.debug("Admin selected to view all refugees at selected camp.")
            print("Refugees at plan", plan_id + ",", camp_name + ":")
            print("Refugee ID - Refugee Name - Date of Birth - # Family Members")
            for row in range(len(refugees.index)):
                print(refugees['refugee_id'].iloc[row], refugees['refugee_name'].iloc[row],
                      refugees['date_of_birth'].iloc[row],
                      str(refugees['family_members'].iloc[row]) + " family members", sep=" - ")
            print("")
            continue
        try:
            refugee_id = int(refugee_id)
            if refugee_id not in refugees['refugee_id'].values:
                raise ValueError
        except ValueError:
            print("Refugee ID not found. Please enter again.")
            logging.error("Invalid user input.")
            continue
        return refugee_id

# allows user to choose whether to enter username directly or go through plan->camp->refugee
def initial_selection():
    """
    Prompts the admin to choose whether to select a refugee by entering the refugee ID directly or selecting a humanitarian plan and camp first.
    If the admin chooses to enter the refugee ID directly, they are prompted for it.
    The function checks whether there are any refugees that can be selected and returns the admin to the previous menu if not.
    """
    while True:
        refugees = pd.read_csv(os.path.join('data', 'refugees.csv'))
        if len(refugees.index) == 0:
            logging.warning("No refugees to select from.")
            print("There are currently no refugees at humanitarian plans.")
            return 0

        logging.debug("Admin prompted to choose between entering refugee ID directly and selecting plan and camp first.")
        print("\nEnter [1] to select a refugee by entering the refugee ID directly")
        print("Enter [2] to filter by plan and camp before selecting a refugee")
        print("Enter [0] to return to the previous menu")
        try:
            option = int(input("Select an option: "))
            if option not in range(3):
                raise ValueError
        except:
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        if option in (0, 2):
            return option

        # select refugee directly
        logging.debug("Admin prompted to enter refugee ID.")
        while True:
            print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
            refugee_id = input("Enter the refugee ID of your chosen refugee: ")
            if refugee_id.upper() == "X":
                return 0
            if refugee_id.upper() == "B":
                refugee_id = "B"  # in case not upper; so that refugee_id == "B" comparison can be done below
                break
            try:
                refugee_id = int(refugee_id)
                if refugee_id not in refugees['refugee_id'].values:
                    raise ValueError
            except ValueError:
                print("Refugee ID not found. Please enter again.\n")
                logging.error("Invalid user input.")
                continue
            break

        if refugee_id == "B":
            logging.debug("Returning to previous step.")
            continue
        selected = refugees[refugees['refugee_id'] == refugee_id]
        return selected.iloc[0]['plan_id'], selected.iloc[0]['camp_name'], refugee_id

# for admin methods requiring volunteer to be selected at the start (but no further progress loop)
# returns 0 if user chooses to return to previous memu
def select_plan_camp_refugee():
    """
    Enables the admin to select a refugee when viewing or editing refugee's profiles.
    """
    progress = 0
    while progress < 4:
        if progress == 0:
            refugee = initial_selection()
            if refugee == 0:
                return 0
            elif refugee == 2:
                progress += 1
            else:
                return refugee

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
            camp_name = select_camp(plan_id)
            if camp_name == "X":
                return 0
            elif camp_name == "B":
                logging.debug("Returning to previous step.")
                progress -= 1
            else:
                progress += 1

        if progress == 3:
            refugee_id = select_refugee(plan_id, camp_name)
            if refugee_id == "X":
                return 0
            elif refugee_id == "B":
                logging.debug("Returning to previous step.")
                progress -= 1
            else:
                progress += 1

    return plan_id, camp_name, refugee_id
