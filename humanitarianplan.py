import logging

class HumanitarianPlan:
    """
    Class for the Humanitarian Plan. It requires a description, location, start_date and nb_of_camps which are passed
    as arguments from create_hum_plan method of Admin class.

    nb_of_camps is the number of camps created when the Humanitarian Plan is created. The admin should specify how
    many camps should be set up.

    When initialised, end_date is set to 'None' and can later be edited with edit_end_date method of Admin class.

    When initialised, a resources csv file is created with a row for the number of camps specified
    """

    def __init__(self, description, location, start_date, nb_of_camps):
        self.description = description
        self.location = location
        self.start_date = start_date
        self.name = f'{location}_{start_date[6:]}'  # name would be location + year e.g. United Kingdom 2023
        self.nb_of_camps = int(nb_of_camps)
        self.end_date = None  # end_date will be redefined with end_event method from Admin class

        # When a Humanitarian Plan object is created, it also creates 2 .csv files for that HP
        create = open(f"{self.name}.csv", "w") #this one for general info + CURRENT amount of resources in each camp (can be edited by volunteers/admin)
        create.write("camp_name,volunteers,refugees,capacity,food,water,firstaid_kits")
        create.close()
        # resources = open(f"{self.name}_resources.csv", "w") #this one for resources specifically: how much in storage and how much ALLOCATED to each camp by admin
        # resources.write("location,food_packs,water,firstaid_kits"
        #                 "\nStorage,100,100,25") # default amount of resources
        # for i in range(1, self.nb_of_camps + 1):  # starts at 1 since default is 0 and doesn't make sense to have Camp 0
        #     resources.write(f"\nCamp {i},0,0,0")
        # resources.close()

        # Adds the rows for each camp into the resources.csv file, based on how many camps exist
        # e.g. if nb_of_camps is 3, there will be a row added to the csv for Camp 1, Camp 2, and Camp 3
        add_camps = open(f"{self.name}.csv", "a")
        for i in range(1, self.nb_of_camps + 1):  # starts at 1 since default is 0 and doesn't make sense to have Camp 0
            add_camps.write(f"\nCamp {i},0,0,0,0,0,0")  # at the start, each camp has 0 of every resource type

        logging.debug("Created for csv file for the humanitarian plan's camps.")
