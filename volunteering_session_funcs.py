import datetime
import logging

def select_date():
    logging.debug("User prompted to select date of volunteering session.")
    while True:
        print("You can add volunteering sessions within the next 2 weeks, starting from tomorrow.")
        start_date = datetime.date.today() + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=13)
        print("Available dates: " + start_date.strftime('%d-%m-%Y') + " to " + end_date.strftime('%d-%m-%Y'))

        print("\nEnter [0] to return to the previous menu.")
        vol_date = input(
            "Enter the date of the volunteering session in the format DD-MM-YYYY: ").strip()
        if vol_date == "0":
            return vol_date
        try:
            vol_dt = datetime.datetime.strptime(vol_date, "%d-%m-%Y").date()
        except ValueError:
            print("Incorrect date format. Please use the format DD-MM-YYYY (e.g. 18-11-2023).")
            logging.error("Invalid user input.")
            continue
        if vol_dt < start_date or vol_dt > end_date:
            print("Please enter a date from " + start_date.strftime('%d-%m-%Y') + " to " + end_date.strftime(
                '%d-%m-%Y') + " (inclusive).")
            logging.error("Date entered is outside the acceptable range.")
            continue
        return datetime.datetime.strftime(vol_dt, '%Y-%m-%d')  # e.g. 2023-11-18


def select_start_time(vol_date, cur_user_times):
    vol_date2 = datetime.datetime.strptime(vol_date, '%Y-%m-%d').date().strftime('%d-%m-%Y')

    prev_day = datetime.datetime.strptime(vol_date, '%Y-%m-%d').date() - datetime.timedelta(days=1)
    prev_day1 = prev_day.strftime('%Y-%m-%d') + " 23:30"
    next_day = datetime.datetime.strptime(vol_date, '%Y-%m-%d').date() + datetime.timedelta(days=1)
    next_day1 = next_day.strftime('%Y-%m-%d') + " 00:00"
    next_day2 = next_day.strftime('%Y-%m-%d') + " 00:30"

    booked_slots = cur_user_times[(cur_user_times['start_time'].str.startswith(vol_date)) |
                                  (cur_user_times['start_time'] == next_day1) |
                                  (cur_user_times['start_time'] == next_day2) |
                                  (cur_user_times['end_time'].str.startswith(vol_date)) |
                                  (cur_user_times['end_time'] == prev_day1)]

    logging.debug("User is shown any existing volunteering sessions that affect available start times on the selected date.")
    if len(booked_slots.index) == 0:
        print("\nYou have not added any volunteering sessions on or affecting", vol_date2 + " yet.")
    else:
        print("\nYou have added the following volunteering sessions:")
        # print existing times affecting the selected date, switching from YYYY-MM-DD to DD-MM-YYYY
        for row in range(len(booked_slots.index)):
            print("Start:",
                  datetime.datetime.strptime(booked_slots['start_time'].iloc[row], "%Y-%m-%d %H:%M").strftime(
                      "%d-%m-%Y %H:%M"), "\t", "End:",
                  datetime.datetime.strptime(booked_slots['end_time'].iloc[row], "%Y-%m-%d %H:%M").strftime(
                      "%d-%m-%Y %H:%M"))

    print("\nYou are welcome to volunteer at any time of the day.")
    print("Note that all volunteering sessions must start on the hour or half past (e.g. 09:00, 15:30).")
    print("Each volunteering session must be a multiple of 30 minutes, up to a maximum of 5 hours.")
    print(
        "There must be at least 1 hour between volunteering sessions. Please cancel your existing sessions first if necessary.")

    logging.debug("Generating list of available start times.")
    # generate list of available start times based on conditions above
    available = []
    for time in [datetime.time(h, m).strftime('%H:%M') for h in range(0, 24) for m in (0, 30)]:
        time_str = vol_date + " " + time  # e.g. 2023-11-18 00:30
        time_d = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        for row in range(len(booked_slots.index)):
            if (time_d >= datetime.datetime.strptime(booked_slots['start_time'].iloc[row],
                                                     "%Y-%m-%d %H:%M") - datetime.timedelta(hours=1)
                    and time_d < datetime.datetime.strptime(booked_slots['end_time'].iloc[row],
                                                            "%Y-%m-%d %H:%M") + datetime.timedelta(hours=1)):
                break
        else:
            available.append(time)

    if len(available) == 0:
        print("No available start times on the selected date. Please select another date.")
        logging.warning("No available start times on the selected date. Returning to previous step.")
        return "9"

    logging.debug("User prompted to enter start time of volunteering session.")
    while True:
        print("\nEnter [0] to return to the previous menu or [9] to go back to the previous step.")
        print("Enter [1] to show all available start times.")
        start = input(
            "Enter the start time of the volunteering session in the format HH:mm (e.g. 14:00): ").strip()
        if start in ("0", "9"):
            return start
        if start == "1":
            print("\nThe following start times are available on", vol_date2 + ":")
            print(", ".join(available))
            logging.debug("User has chosen to view all available start times.")
            continue
        if start not in available:
            print("Please enter an available start time in the format HH:mm.")
            logging.error("Invalid user input.")
            continue
        return vol_date + " " + start  # e.g. 2023-11-18 00:30


def select_end_time(start_time, cur_user_times):
    # find next slot booked after start time
    next_slot = cur_user_times[cur_user_times['start_time'] > start_time].head(1)
    logging.debug("Generating list of available start times.")
    # generate list of available end times
    available_end = []
    st = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    for step in range(1, 11):
        time_d = st + datetime.timedelta(minutes=30 * step)
        if len(next_slot.index) > 0:
            if time_d > datetime.datetime.strptime(next_slot['start_time'].iloc[0],
                                                   "%Y-%m-%d %H:%M") - datetime.timedelta(hours=1):
                break
        time = time_d.strftime('%d-%m-%Y %H:%M')
        available_end.append(time)

    logging.debug("User prompted to select end time of volunteering session.")
    while True:
        print("\nEnter [X] to return to the previous menu or [B] to go back to the previous step.")
        print("Choose the end time of the volunteering session.")
        for i, time in enumerate(available_end):
            print("[" + str(i + 1) + "] " + time)
        end = input("Enter the number of your chosen end time: ").strip()
        if end.upper() in ("X", "B"):
            return end.upper()
        try:
            end = int(end)
            if end not in range(1, len(available_end) + 1):
                raise ValueError
        except ValueError:
            print("Please enter a number corresponding to one of the available end times.")
            logging.error("Invalid user input.")
            continue
        end_time = available_end[end - 1]
        return datetime.datetime.strptime(end_time, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M')


def confirm_slot(start_time, end_time):
    start_time2 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
    end_time2 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M')
    print("\nYou are adding the following volunteering session:")
    print("Start:", start_time2)
    print("End:", end_time2)
    duration = str(
        datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M") - datetime.datetime.strptime(start_time,
                                                                                            "%Y-%m-%d %H:%M"))
    if duration[0] == 0:
        dur_str = ""
    elif duration[0] == "1":
        dur_str = duration[0] + " hour"
    else:
        dur_str = duration[0] + " hours"
    if duration[2:4] == "30":
        dur_str += " 30 minutes"
    print("Duration:", dur_str)

    logging.debug("User prompted to confirm details of volunteering session to be added.")
    while True:
        print("\nEnter [1] to confirm")
        print("Enter [9] to go back to the previous step")
        print("Enter [0] to cancel and return to the previous menu")
        try:
            option = int(input("Select an option: "))
            if option not in (0, 1, 9):
                raise ValueError
        except ValueError:
            print("Please enter a number from the options provided.")
            logging.error("Invalid user input.")
            continue
        return option