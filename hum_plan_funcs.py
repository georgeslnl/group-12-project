import re, logging, datetime, pandas as pd
import verify as v

def add_description():
    logging.debug("Admin prompted to enter description.")
    while True:
        print("\nEnter [0] to return to the previous menu.")
        try:
            desc = input("Please enter a description of the event: ").strip()
            if desc == "0":
                return desc
            s = re.search("[a-zA-Z]", desc)
            if not s:
                raise ValueError
        except ValueError:
            print("Please ensure description contains text.")
            logging.error("Invalid user input.")
            continue
        if len(desc) > 200:
            print("Description cannot exceed 200 characters.")
            logging.error("Description entered is too long.")
            continue
        return desc

def add_location():
    logging.debug("Admin prompted to enter location.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        try:
            loc = input("Please enter the location (city) of the event: ").strip()
            if loc in ("0", "9"):
                return loc
            s = re.search("[a-zA-Z]", loc)
            if not s:
                raise ValueError
        except ValueError:
            print("Please ensure location contains text.")
            logging.error("Invalid user input.")
            continue
        if loc.lower() not in v.valid_cities:
            print("The city you have entered does not exist. Please try again.")
            logging.error("Location entered is not a valid city name.")
            continue
        return loc

def add_start_date(location):
    logging.debug("Admin prompted to enter start date of plan.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        start_date = input("Please enter the start date of the event (DD-MM-YYYY): ").strip()
        if start_date in ("0", "9"):
            return start_date
        try:
            start = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
        except ValueError:
            print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 23-07-1999).")
            logging.error("Invalid user input.")
            continue
        t = datetime.date.today()
        if start > t:
            print("Start date cannot be in the future. Please try again.")
            logging.error("Admin entered a start date in the future.")
            continue
        new_id = location + "_" + start_date[6:]
        plans = pd.read_csv("humanitarian_plan.csv")
        if new_id in plans['plan_id'].values:
            print("There is already a humanitarian plan with plan ID", new_id + ",",
                  "i.e. location in", location, "and start date in", start_date[6:] + ".",
                  "\nYou will be prompted to re-enter the location.")
            logging.error("plan_id (location and start date) already exists.")
            return "9"
        if start < t - datetime.timedelta(days=30):
            logging.warning("Admin entered a start date more than 30 days in the past.")
            logging.debug("Admin prompted to confirm start date.")
            while True:
                print("\nWarning: More than 30 days have elapsed since the start date.")
                print("Do you wish to proceed?")
                print("Enter [1] to proceed")
                print("Enter [9] to re-enter start date")
                try:
                    option = int(input("Select an option: "))
                    if option not in (1, 9):
                        raise ValueError
                except ValueError:
                    print("Please enter a number from the options provided.")
                    logging.error("Invalid user input.")
                    continue
                logging.debug("Start date confirmed.")
                break
            if option == 9:
                continue
        return start_date


def add_num_camps():
    while True:
        print("\nEnter [X] to return to the previous menu or B] to go back to the previous step.")
        nb_of_camps = input("The maximum number of camps is 15."
                            "\nPlease enter the number of camps to set up: ").strip()
        if nb_of_camps.upper() in ("X", "B"):
            return nb_of_camps.upper()
        try:
            nb_of_camps = int(nb_of_camps)
            if nb_of_camps <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a positive integer.")
            logging.error("Invalid user input.")
            continue
        if nb_of_camps > 15:
            print("Number of camps cannot exceed 15.")
            logging.error("Number of camps entered is more than 15.")
        return nb_of_camps

def edit_description(plan_id, cur_desc):
    print(f'You have chosen to edit the description of {plan_id}.'
          f'\n The current description is:'
          f'\n {cur_desc}')
    logging.debug("Admin prompted to enter new description.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        try:
            new_desc = input(f'Enter the new description of {plan_id}: ').strip()
            if new_desc in ("0", "9"):
                return new_desc
            s = re.search("[a-zA-Z]", new_desc)
            if not s:
                raise ValueError
        except ValueError:
            print("Please ensure description contains text.")
            logging.error("Invalid user input.")
            continue
        if new_desc == cur_desc:
            print("Description is unchanged. Please try again.")
            logging.error("Description is unchanged.")
            continue
        if len(new_desc) > 200:
            print("Description cannot exceed 200 characters.")
            logging.error("Description entered is too long.")
            continue
        # new_desc will be updated in the csv file after being returned
        return new_desc


def edit_no_camps(plan_id, plan_index, hum_plan_df, plan_df, num_camps):
    '''
   This function allows admin to open or close camps within a humanitarian plan.
   If admin chooses to close camps, they can choose to reallocate refugees, volunteers and resources belonging
   to those camps.
   If admin chooses to open camps, they have 0 refugees, volunteers, capacity and resources by default -
   admin can choose to edit these details by choosing from the main menu.
    '''
    while True:
        print("\nEnter [0] to return to the previous menu.")
        new_num = v.integer(f'The maximum number of camps is 15.'
                            f'\nEnter the new number of camps for {plan_id}: ')
        if new_num == 0:
            return new_num
        elif new_num not in range(1, 16):
            print('Please enter an integer between 1 and 15.')
        elif new_num == num_camps:
            print('Number entered is equal to the current number of camps. '
                  'Please enter a different integer between 1 and 15.')
        else:
            break
    hum_plan_df.loc[hum_plan_df.index == plan_index, "number_of_camps"] = new_num
    print(f'The updated details of {plan_id} are as follows:'
          f'\n{hum_plan_df.loc[hum_plan_df.index == plan_index, :]}')
    difference = new_num - num_camps
    if difference < 0:
        difference = abs(difference)
        closed_camps_reverse = []
        for d in range(0, difference):
            closed_camps_reverse.append(f'Camp {num_camps - d}')
        closed_camps = closed_camps_reverse[::-1]
        print(f'You have chosen to set the number of camps to {new_num}, '
              f'this means you are closing {closed_camps}.')
        while True:
            choice = v.string(f'Please choose whether you would like to reallocate the refugees, volunteers and '
                              f'resources belonging to these camps.'
                              f'\nIf you choose to, these refugees evenly divided amongst the other camps '
                              f'(capacity allowing), \nvolunteers will be disaffiliated with any camps, '
                              f'and the resources will be moved back to storage.'
                              f'\nIf you choose not to, these refugees, volunteers and resources '
                              f'will be removed from the plan.'
                              f'\nEnter [Y] for yes, [N] for no.')
            if choice != 'Y' and choice != 'N':
                print('Please enter [Y] for reallocating refugees, volunteers and resources, [N] for no.')
            else:
                if choice == 'N':
                    #need to figure out what happens to refugees and volunteers
                    # remove camp rows for closed camps in plan.csv
                    plan_df = plan_df[-plan_df['camp_name'].isin(closed_camps)]
                    return
                # not sure if it's a good idea for refugees and resources to just disappear before the plan is closed!
                # this step could possibly just be a confirmation after reminding the admin that refugees will be reallocated etc?
                break
        if choice == 'Y':
            refugee_df = pd.read_csv('refugees.csv')
            volunteer_df = pd.read_csv('users.csv')
            # can't close camps if not enough remaining capacity
            closed_camps_df = plan_df[plan_df.camp_name.isin(closed_camps)]
            open_camps_df = plan_df[plan_df.camp_name.isin(closed_camps) == False]
            total_remaining_capacity = sum(open_camps_df.capacity) - sum(open_camps_df.refugees)
            total_displaced = 0
            for camp in range(len(closed_camps_df)):
                total_displaced += closed_camps_df.iloc[camp, 2]
            if total_displaced > total_remaining_capacity:
                print('Total number of displaced refugees is less than the total remaining capacity of the remaining '
                      'camps.'
                      '\nPlease edit the capacity of the remaining camps before closing camps. '
                      '\nChanges to the camp number have not been saved.')
                return
            else:
                print('The change of number of camps has been saved.')
                hum_plan_df.to_csv('humanitarian_plan.csv', index=False)
            # dict of camps and remaining capacity, sort by highest to lowest capacity, iterate through each family and
            # allocate each to the camp with highest remaining capacity
            remaining_capacity = dict(zip(open_camps_df.camp_name, (open_camps_df.capacity - open_camps_df.refugees)))
            print('Reallocating refugee families from closed camps to remaining camps...')
            for camp in closed_camps:
                print(f'List of reallocated refugee families from {camp} (in format (refugee_id, new_camp)):')
                for refugee_family in refugee_df.iterrows():
                    refugee_id = refugee_family[1]['refugee_id']
                    if refugee_family[1]['camp_name'] == camp:
                        reassigned_camp = max(remaining_capacity, key=remaining_capacity.get)
                        refugee_df.loc[refugee_df.refugee_id == refugee_id, 'camp_name'] = reassigned_camp
                        remaining_capacity[reassigned_camp] -= refugee_family[1]['family_members']
                        plan_df.loc[plan_df.camp_name == reassigned_camp, 'refugees'] += refugee_family[1][
                            'family_members']
                        plan_df.loc[plan_df.camp_name == camp, 'refugees'] -= refugee_family[1]['family_members']
                        print(refugee_id, reassigned_camp)
            # if family cannot fit into the camp with largest remaining capacity?
            # -> during loop, if remaining_capacity[reassigned_camp] < refugee_family[1]['family_members']: print message and return
            # volunteer - just change camp name to NaN if volunteer's camp is closed
            print('The camp name of all volunteers in camps that are being closed will be set to [NaN].')
            for camp in closed_camps:
                for volunteer in volunteer_df.iterrows():
                    username = volunteer[1]['username']
                    if volunteer[1]['camp_name'] == camp:
                        volunteer_df.loc[volunteer_df.username == username, 'camp_name'] = None
                        plan_df.loc[plan_df.camp_name == camp, 'volunteers'] -= 1
            # TODO: remove all volunteering sessions for the given plan_id and camp here
            # resources - add back to storage
            print('Resources (food packs, water and first-aid kits) of camps being closed will be moved back to storage '
                  'in the same plan.')
            for camp in closed_camps:
                hum_plan_df.iloc[plan_index, -3] += plan_df.loc[plan_df.camp_name == camp, 'food']
                plan_df.loc[plan_df.camp_name == camp, 'food'] = 0
                hum_plan_df.iloc[plan_index, -2] += plan_df.loc[plan_df.camp_name == camp, 'water']
                plan_df.loc[plan_df.camp_name == camp, 'water'] = 0
                hum_plan_df.iloc[plan_index, -1] += plan_df.loc[plan_df.camp_name == camp, 'firstaid_kits']
                plan_df.loc[plan_df.camp_name == camp, 'firstaid_kits'] = 0
            #remove camp rows for closed camps in plan.csv
            plan_df = plan_df[-plan_df['camp_name'].isin(closed_camps)]
            refugee_df.to_csv('refugees.csv', index=False)
            volunteer_df.to_csv('users.csv', index=False)
            plan_df.to_csv(f'{plan_id}.csv', index=False)
            hum_plan_df.to_csv('humanitarian_plan.csv', index=False)
            return
    elif difference > 0:
        print(f'You have chosen to set the number of camps to {new_num}, '
              f'this means you are opening {difference} camps.'
              f'\nPlease note new camps have 0 refugees, volunteers, capacity and resources.'
              f'You can change this by choosing to do so on the main menu.')
        for i in range(1, difference + 1):
            add_camps = open(f"{plan_id}.csv", "a")
            add_camps.write(f"\nCamp {num_camps + i},0,0,0,0,0,0")
        add_camps.close()
        # should we instead set the new camp numbers to start from 1 more than the current largest camp number?
        # if a camp was removed previously, so e.g. the remaining camps are 1,2,4,5,
        # then num_camps + 1 = 5, but Camp 5 is already taken
        new_plan = pd.read_csv(f"{plan_id}.csv")
        print(f'The change has been saved. The updated details of {plan_id} are as follows:'
              f'\n{new_plan}')
        return
