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
        camp_num = int(input("Enter the number of your chosen camp: "))
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
