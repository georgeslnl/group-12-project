import pandas as pd, os
import logging

def edit_food(plan_id, camp_name):
    """
    Prompts the user to enter the number of food packets consumed at the selected camp.
    The user is asked for confirmation before the update is applied.
    """
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    my_camp = camps[camps['camp_name'] == camp_name]
    cur_food = my_camp.iloc[0]['food']
    print("\nCurrent supply of food packets at " + plan_id + ", " + camp_name + ": " + str(cur_food))

    logging.debug("User prompted to enter number of food packets consumed.")
    while True:
        print("Enter [X] to return to the previous step.")
        food_consumed = input(">>Enter the number of food packets consumed: ")
        if food_consumed.upper() == "X":
            logging.debug("Returning to previous step.")
            return
        try:
            food_consumed = int(food_consumed)
            if food_consumed <= 0:
                raise ValueError
        except ValueError:
            print("\nPlease enter a positive integer.")
            logging.error("Invalid user input.")
            continue
        if food_consumed > cur_food:
            print("\nFood consumed exceeds the current supply. "
                  "Please try again or return to the previous step.")
            continue

        # confirmation
        logging.debug("User prompted for confirmation.")
        while True:
            print("\nConfirmation:", food_consumed, "out of", cur_food, "food packets have been consumed.")
            print("Proceed to update camp information?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the previous step\n")
            try:
                confirm = int(input(">>Select an option: "))
                if confirm not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break
        if confirm == 0:
            logging.debug("Returning to previous step.")
            continue
        break
    logging.debug("Consumption of food confirmed.")
    # update csv file
    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'food'] = cur_food - food_consumed
    camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
    logging.debug("updated camps csv file")
    print("\nFood supply updated successfully!")
    print("Updated supply of food packets:", cur_food - food_consumed)
    return

def edit_water(plan_id, camp_name):
    """
    Prompts the user to enter the number of water portions consumed at the selected camp.
    The user is asked for confirmation before the update is applied.
    """
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    my_camp = camps[camps['camp_name'] == camp_name]
    cur_water = my_camp.iloc[0]['water']
    print("\nCurrent supply of water portions at " + plan_id + ", " + camp_name + ": " + str(cur_water))

    logging.debug("User prompted to enter number of water portions consumed.")
    while True:
        print("Enter [X] to return to the previous step.\n")
        water_consumed = input(">>Enter the number of water portions consumed: ")
        if water_consumed.upper() == "X":
            logging.debug("Returning to previous step.")
            return
        try:
            water_consumed = int(water_consumed)
            if water_consumed <= 0:
                raise ValueError
        except ValueError:
            print("\nPlease enter a positive integer.")
            logging.error("Invalid user input.")
            continue
        if water_consumed > cur_water:
            print("\nWater consumed exceeds the current supply. Please try again or return to the previous step.")
            continue

        # confirmation
        logging.debug("Admin prompted for confirmation.")
        while True:
            print("\nConfirmation:", water_consumed, "out of", cur_water, "water portions have been consumed.")
            print("Proceed to update camp information?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the previous step\n")
            try:
                confirm = int(input(">>Select an option: "))
                if confirm not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break
        if confirm == 0:
            logging.debug("Returning to previous step.")
            continue
        break
    logging.debug("Consumption of water confirmed.")
    # update csv file
    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'water'] = cur_water - water_consumed
    camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
    logging.debug("updated camps csv file")
    print("\nWater supply updated successfully!")
    print("Updated supply of water portions:", cur_water - water_consumed)
    return

def edit_medical_supplies(plan_id, camp_name):
    """
    Prompts the user to enter the number of first-aid kits used at the selected camp.
    The user is asked for confirmation before the update is applied.
    """
    camps = pd.read_csv(os.path.join('data', plan_id + '.csv'))
    my_camp = camps[camps['camp_name'] == camp_name]
    cur_medical = my_camp.iloc[0]['firstaid_kits']
    print("\nCurrent supply of first-aid kits at " + plan_id + ", " + camp_name + ": " + str(cur_medical))

    logging.debug("User prompted to enter number of first-aid kits used.")
    while True:
        print("Enter [X] to return to the previous step.\n")
        medical_used = input(">>Enter the number of first-aid kits used: ")
        if medical_used.upper() == "X":
            logging.debug("Returning to previous step.")
            return
        try:
            medical_used = int(medical_used)
            if medical_used <= 0:
                raise ValueError
        except ValueError:
            print("\nPlease enter a positive integer.")
            logging.error("Invalid user input.")
            continue
        if medical_used > cur_medical:
            print("\nFirst-aid kits used exceed the current supply. "
                  "\nPlease try again or return to the previous step.")
            continue

        # confirmation
        logging.debug("User prompted for confirmation.")
        while True:
            print("\nConfirmation:", medical_used, "out of", cur_medical, "first-aid kits have been used.")
            print("Proceed to update camp information?")
            print("Enter [1] to proceed")
            print("Enter [0] to return to the previous step\n")
            try:
                confirm = int(input(">>Select an option: "))
                if confirm not in (0, 1):
                    raise ValueError
            except ValueError:
                print("\nPlease enter a number from the options provided.")
                logging.error("Invalid user input.")
                continue
            break
        if confirm == 0:
            logging.debug("Returning to previous step.")
            continue
        break
    logging.debug("Consumption of first-aid kits confirmed.")
    # update csv file
    chosen = (camps['camp_name'] == camp_name)
    camps.loc[chosen, 'firstaid_kits'] = cur_medical - medical_used
    camps.to_csv(os.path.join('data', plan_id + '.csv'), index=False)
    logging.debug("updated camps csv file")
    print("\nSupply of first-aid kits updated successfully!")
    print("Updated supply of first-aid kits:", cur_medical - medical_used)
    return
