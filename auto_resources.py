import pandas as pd, numpy as np
from datetime import datetime
import admin
import verify as v
import logging

def auto_all(hum_plan, location):
    resources = pd.read_csv(hum_plan)
    humani_plan = pd.read_csv("humanitarian_plan.csv")

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
        # each person consumes 1/3 kit per day (presumably)
        firstaid_needed = int((refugees * 7) / 3) - resources.loc[i, "firstaid_kits"]
        if firstaid_needed < 0:
            firstaid_needed = 0
        sum_needed[2] += firstaid_needed

    # check if we have enough resources in store.
    food_in_storage = int(humani_plan.loc[humani_plan.location == location, 'food_storage'].iloc[0])
    # add .iloc[0] at the end if needed to get one single value
    water_in_storage = int(
        humani_plan.loc[humani_plan['location'] == location, 'water_storage'].iloc[0])
    firstaid_in_storage = int(
        humani_plan.loc[humani_plan['location'] == location, 'firstaid_kits_storage'].iloc[0])
    # if storage resources insufficient
    if food_in_storage < sum_needed[0] or water_in_storage < sum_needed[1] or firstaid_in_storage < sum_needed[2]:
        print("Resources insufficient, please enter manually or request new resources.")
        admin.resources_menu()

    # now we add and write one by one, if resources sufficient
    else:
        while True:
            confirm = input(f"{sum_needed[0]} of food, {sum_needed[1]} of water, "
                            f"and {sum_needed[2]} of first-aid kits will be added to camps from storage.\n"
                            f"Would you like to proceed? (Y/N)\n").capitalize()
            if confirm == "Y":
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
                    firstaid_needed = int((refugees * 7) / 3) - resources.loc[i, "firstaid_kits"]
                    humani_plan.loc[
                        humani_plan['location'] == location, 'firstaid_kits_storage'] -= firstaid_needed
                    resources.loc[i, "firstaid_kits"] += firstaid_needed
                    # write each iterate into two .csv
                    resources.to_csv(hum_plan, index=False)
                    humani_plan.to_csv("humanitarian_plan.csv", index=False)
                print(f"\nAllocation complete. Currently, the resources in {hum_plan[:-4]} are as follows:"
                      f"\n{resources}")
                print(f"\nAnd the remaining resources in storage: "
                      f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
                exit()  # TODO use something else
            elif confirm == "N":
                print("Now returning to resources menu.")
                exit()  # TODO where should I lead to?
            else:
                print("Please enter the correct input (Y/N)")

def auto_one(hum_plan, location):
    resources = pd.read_csv(hum_plan)
    humani_plan = pd.read_csv("humanitarian_plan.csv")
    print(resources.to_string(index=False))
    while True:
        camp_no = v.integer("\nPlease enter the camp number where you would like to allocate resources to.\n")
        camp_name = f"Camp {camp_no}"
        if not any(resources['camp_name'].str.contains(f"Camp {camp_no}")):
            print('The camp ID you entered does not belong to any existing camp in this humanitarian plan.')
        else:
            refugees = int(resources.loc[resources['camp_name'] == camp_name, "refugees"].iloc[0])
            food_needed = refugees * 7 - int(resources.loc[resources['camp_name'] == camp_name, "food"].iloc[0])
            if food_needed < 0:  # if we have more than 7 days, no need to top-up
                food_needed = 0
            water_needed = refugees * 7 - int(resources.loc[resources['camp_name'] == camp_name, "water"].iloc[0])
            if water_needed < 0:
                water_needed = 0
            # each person consumes 1/3 kit per day (presumably)
            firstaid_needed = int((refugees * 7) / 3) - int(
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
                auto_one()

            # now we add and write one by one, if resources sufficient
            else:
                while True:
                    confirm = input(f"{food_needed} of food, {water_needed} of water, "
                                    f"and {firstaid_needed} of first-aid kits will be added to {camp_name} from storage.\n"
                                    f"Would you like to proceed? (Y/N)\n").capitalize()
                    if confirm == "N":
                        print("Now returning to resources menu.")
                        return
                    elif confirm == "Y":
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
                        print(f"\nAllocation complete. Currently, the resources in {hum_plan[:-4]} are as follows:"
                              f"\n{resources}")
                        print(f"\nAnd the remaining resources in storage: "
                              f"\n{humani_plan.loc[humani_plan.location == location, ['location', 'start_date', 'food_storage', 'water_storage', 'firstaid_kits_storage']]}\n")
                        print("Now returning to resources menu.\n")
                        return
                    else:
                        print("Please enter the correct input (Y/N)")