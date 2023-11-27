import pandas as pd, numpy as np
from datetime import datetime
import admin
import verify as v
import logging


# By entering the plan_id and camp_name, we will get how many supplies we need exactly
def med_needed(plan_id, camp_name):
    """
    It iterates through each family's medical condition and family size in order to return the sufficient supplies for the camp per day.
    :param plan_id: 'London_2023' for example
    :param camp_name: 'Camp 4' for example
    :return:
    """
    refugees = pd.read_csv("refugees.csv")
    filtered_refugees = refugees[(refugees['plan_id'] == plan_id) & (refugees['camp_name'] == camp_name)]
    total_med_needed = 0

    # Iterate each refugee
    for index, row in filtered_refugees.iterrows():
        fam_size = row['family_members']    #getting the no. of family memebers
        med_con = str(row['medical_condition']) #getting their medical condition
        # medical condition: 1 is 0, 2/4/6 is 2, 3/5 is 5, 7 is 7
        if med_con == "1":
            med_needed = 0
        elif med_con == "2" or med_con == "4" or med_con == "6":
            med_needed = 1*fam_size
        elif med_con == "3" or med_con == "5":
            med_needed = 2*fam_size
        elif med_con ==  "7":
            med_needed = 3*fam_size
        total_med_needed += med_needed
    return total_med_needed

def auto_all(hum_plan, location):
    """
    It checks remaining resources in storage and distribute resources to camps automatically to top up for each camp's following 7 days according to the conditions in camps.
    If remaining resources insufficient, system will suggest manual allocation or request new resources to storage.
    :param hum_plan: 'London_2023.csv' for example
    :param location: 'London' for example
    :return:
    """
    resources = pd.read_csv(hum_plan) # hum_plan == London_2023.csv for example
    humani_plan = pd.read_csv("humanitarian_plan.csv")

    logging.debug("Calculating the amount of each resource needed to top up all camps to 7 days of supplies.")
    # first we count how many resources we need
    sum_needed = [0, 0, 0]  # food, water, firstaid_kits
    for i in resources.index:
        refugees = resources.loc[i, "refugees"]
        food_needed = refugees * 7 - resources.loc[i, "food"]
        if food_needed < 0:  # if we have more than 7 days, no need to top-up
            food_needed = 0
        sum_needed[0] += food_needed
        water_needed = refugees * 7 - resources.loc[i, "water"]
        if water_needed < 0:
            water_needed = 0
        sum_needed[1] += water_needed

        # now we calculate the medical supplies needed
        camp_name = resources.loc[i, "camp_name"]
        firstaid_needed = med_needed(hum_plan[:-4], camp_name)*7 - resources.loc[i, "firstaid_kits"]
        if firstaid_needed < 0:
            firstaid_needed = 0
        sum_needed[2] += firstaid_needed

    # medical condition: 1 is 0, 2/4/6 is 2, 3/5 is 5, 7 is 7

    # check if we have enough resources in store.
    food_in_storage = int(humani_plan.loc[humani_plan.location == location, 'food_storage'].iloc[0])
    # add .iloc[0] at the end if needed to get one single value
    water_in_storage = int(
        humani_plan.loc[humani_plan['location'] == location, 'water_storage'].iloc[0])
    firstaid_in_storage = int(
        humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'].iloc[0])
    # if storage resources insufficient
    if food_in_storage < sum_needed[0] or water_in_storage < sum_needed[1] or firstaid_in_storage < sum_needed[2]:
        print("\nResources insufficient, please enter manually or request new resources.")
        logging.warning("Insufficient resources in storage. Unable to auto-allocate.")
        return

    # now we add and write one by one, if resources sufficient
    logging.debug("Admin prompted to confirm auto-allocation.")
    while True:
        print(f"\nA total of {sum_needed[0]} food packets, {sum_needed[1]} water portions "
            f"and {sum_needed[2]} first-aid kits will be added to camps from storage.")
        print("Would you like to proceed?")
        confirm = input("Enter [Y] or [N]: ").capitalize()
        if confirm == "Y":
            logging.debug("Auto-allocation confirmed. Resources will be topped up to each camp in turn.")
            for i in resources.index:
                refugees = resources.loc[i, "refugees"]
                # food
                food_needed = refugees * 7 - resources.loc[i, "food"]
                humani_plan.loc[humani_plan['location'] == location, 'food_storage'] -= food_needed
                resources.loc[i, "food"] += food_needed
                # water
                water_needed = refugees * 7 - resources.loc[i, "water"]
                humani_plan.loc[
                    humani_plan['location'] == location, 'water_storage'] -= water_needed
                resources.loc[i, "water"] += water_needed
                # first-aid
                firstaid_needed = med_needed(hum_plan[:-4], camp_name)*7 - resources.loc[i, "firstaid_kits"]
                humani_plan.loc[
                    humani_plan['location'] == location, 'firstaid_kits_storage'] -= firstaid_needed
                resources.loc[i, "firstaid_kits"] += firstaid_needed
                # write each iterate into two .csv
                resources.to_csv(hum_plan, index=False)
                humani_plan.to_csv("humanitarian_plan.csv", index=False)
            logging.debug("Auto-allocation complete. humanitarian_plan.csv and camps csv file updated.")
            print(f"\nAllocation complete. Currently, the resources in {hum_plan[:-4]} are as follows:"
                  f"\n{resources}")
            print(f"\nAnd the remaining resources in storage: "
                  f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
            return
        elif confirm == "N":
            print("Now returning to admin resources menu.")
            logging.debug("Admin did not confirm. Returning to resources menu.")
            return
        else:
            print("Please enter the correct input (Y/N).")
            logging.error("Invalid user input.")

def auto_one(hum_plan, location):
    """
    It checks remaining resources in storage and distribute resources to the selected camp automatically to top up for the following 7 days according to the condition in camp.
    If remaining resources insufficient, system will suggest manual allocation or request new resources to storage.
    :param hum_plan: 'London_2023.csv' for example
    :param location: 'London' for example
    :return:
    """
    resources = pd.read_csv(hum_plan)
    humani_plan = pd.read_csv("humanitarian_plan.csv")
    print(resources.to_string(index=False))
    logging.debug("Admin prompted to select camp.")
    while True:
        camp_no = v.integer("\nEnter [0] to return to the previous menu."
                            "\nEnter the number of the camp to which you would like to allocate resources: ")
        if camp_no == 0:
            logging.debug("Returning to previous menu.")
            return
        camp_name = f"Camp {camp_no}"
        if not any(resources['camp_name'].str.contains(f"Camp {camp_no}")):
            print('Please enter the number of an existing camp in this humanitarian plan.')
            logging.error("Invalid user input.")
            continue

        logging.debug(f"Calculating the amount of each resource needed to top up {camp_name} to 7 days of supplies.")
        refugees = int(resources.loc[resources['camp_name'] == camp_name, "refugees"].iloc[0])
        food_needed = refugees * 7 - int(resources.loc[resources['camp_name'] == camp_name, "food"].iloc[0])
        if food_needed < 0:  # if we have more than 7 days, no need to top-up
            food_needed = 0
        water_needed = refugees * 7 - int(resources.loc[resources['camp_name'] == camp_name, "water"].iloc[0])
        if water_needed < 0:
            water_needed = 0
        # each person consumes 1/3 kit per day (presumably)
        firstaid_needed = med_needed(hum_plan[:-4], camp_name)*7 - int(
            resources.loc[resources['camp_name'] == camp_name, "firstaid_kits"].iloc[0])
        if firstaid_needed < 0:
            firstaid_needed = 0

        # check if we have enough resources in store.
        food_in_storage = int(humani_plan.loc[humani_plan.location == location, 'food_storage'].iloc[0])
        # add .iloc[0] at the end if needed to get one single value
        water_in_storage = int(
            humani_plan.loc[humani_plan['location'] == location, 'water_storage'].iloc[0])
        firstaid_in_storage = int(
            humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'].iloc[0])
        # if storage resources insufficient
        if food_in_storage < food_needed or water_in_storage < water_needed or firstaid_in_storage < firstaid_needed:
            print("Resources insufficient, please request new resources.\n"
                  "Now returning to camp selection.")
            logging.warning("Insufficient resources in storage. Unable to auto-allocate.")
            continue

        # now we add and write one by one, if resources sufficient
        logging.debug(f"Admin prompted to confirm auto-allocation to {camp_name}.")
        while True:
            print(f"\n{food_needed} food packets, {water_needed} water portions "
                  f"and {firstaid_needed} first-aid kits will be added to {camp_name} from storage.")
            print("Would you like to proceed?")
            confirm = input("Enter [Y] or [N]: ").capitalize()
            if confirm == "N":
                print("Now returning to admin resources menu.")
                logging.debug("Admin did not confirm. Returning to resources menu.")
                return
            elif confirm == "Y":
                logging.debug(f"Auto-allocation confirmed. Resources will be topped up to {camp_name}.")
                # food
                humani_plan.loc[humani_plan['location'] == location, 'food_storage'] -= food_needed
                resources.loc[resources['camp_name'] == camp_name, "food"] += food_needed
                # water
                humani_plan.loc[
                    humani_plan['location'] == location, 'water_storage'] -= water_needed
                resources.loc[resources['camp_name'] == camp_name, "water"] += water_needed
                # first-aid
                humani_plan.loc[
                    humani_plan['location'] == location, 'firstaid_kits_storage'] -= firstaid_needed
                resources.loc[resources['camp_name'] == camp_name, "firstaid_kits"] += firstaid_needed
                # write each iterate into two .csv
                resources.to_csv(hum_plan, index=False)
                humani_plan.to_csv("humanitarian_plan.csv", index=False)

                logging.debug("Auto-allocation complete. humanitarian_plan.csv and camps csv file updated.")
                print(f"\nAllocation complete. Currently, the resources in {hum_plan[:-4]} are as follows:"
                      f"\n{resources}")
                print(f"\nAnd the remaining resources in storage: "
                      f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
                return
            else:
                print("Please enter the correct input (Y/N).")
                logging.error("Invalid user input.")