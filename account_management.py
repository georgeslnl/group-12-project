import pandas as pd


def edit_volunteer(self):
    df = pd.read_csv('users.csv')
    # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
    print(df.iloc[1:, 0])
    while True:
        user = v.integer('Please enter the number of the volunteer whose account details you would like to modify. ')
        user = str(user)
        user = "volunteer" + user
        if any(df['username'].str.contains(user)) == True:  # testing if volunteer account already exists
            break
        else:
            print('Number entered does not match any volunteer numbers.')
            continue
    while True:
        # a list for admin to choose from, edited to work for the merged 'users' file
        print("Please choose one of the following details you would like to modify."
              "\n 0 for username"
              "\n 1 for password"
              "\n 2 for active status"
              "\n 3 for first name"
              "\n 4 for last name"
              "\n 5 for email address"
              "\n 6 for phone number"
              "\n 7 for gender"
              "\n 8 for date of birth"
              "\n 9 for plan ID"
              "\n 10 for camp name")
        index = int(v.integer(""))
        if index not in range(0, 11):
            print('Please enter an integer from 0-10.')
            continue
        else:
            # This is code to fix the index problem due to using the new 'users' file
            if index == 2:
                index = 3
            elif index == 0 or index == 1:
                pass
            else:
                index += 2
            break
    temp_list = ['username', 'password', 'account_type', 'active_status', 'deactivation_requested',
                 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'plan_id', 'camp_name']
    new = input("Please enter a new value: ")  # will be used to input into csv as status
    # and then enter a new value
    # create a dataform without that specific row where username is...
    df.loc[df['username'] == user, temp_list[index]] = new  # modify the dataform
    df.to_csv('users.csv', index=False)  # write it into the .csv file
    updated = df['username'] == user
    print("The updated account details of " + user + "is:\n", df[updated])


def create_volunteer(self):
    new = open("users.csv", "a")

    username = v.string("Please enter an user name: ")
    pw = input("Please enter the password: ")  # password should be just '111'
    first_name = v.string("Please enter the first name: ")
    last_name = v.string("Please enter the last name: ")
    email = v.string("PLease enter the email address: ")
    phone = v.integer("Please enter the phone number: ")
    gender = v.integer("Please enter the gender: ")
    DOB = v.date("Please enter the date of birth (DD-MM-YYYY): ")
    plan_id = v.string("Please enter the plan ID: ")
    camp_name = v.string("Please enter the camp name: ")

    new.write(
        f'\n{username},{pw},volunteer,1,0,{first_name},{last_name},{email},{phone},{gender},{DOB},{plan_id},{camp_name}')
    new.close()
    print("New user added successfully.")

    users = pd.read_csv('users.csv')
    new_account = users['username'] == username
    print("The new account details of", username, "is:\n", users[new_account])


def delete_volunteer(self):
    df = pd.read_csv('users.csv')
    # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
    print(df.iloc[1:, 0])
    delete_user = v.integer('Please enter the number of the user you would like to delete. ')
    delete_user = f"volunteer{delete_user}"
    # create a dataform without that specific row where username is...
    df = df[df.username != delete_user]
    df.to_csv('users.csv', index=False)
    print(f"{delete_user} is now deleted.")
    print(df)


def active_volunteer(self):
    while True:
        status = input("Would you like to deactivate or reactivate an user? (D/R)"
                       "\n D for deactivate"
                       "\n R for reactivate")
        status = v.string("")  # will be used to input into csv as status
        _str = ""  # just a placeholder
        if status != "R" and status != "D":
            print("Please enter only D or R.")
        elif status == "R":
            status = "A"
            _str = "reactivate"
            break
        elif status == "D":
            _str = "deactivate"
            break
        else:
            break

    df = pd.read_csv('users.csv')
    # uses pandas to print a table first for selection. So admin doesn't have to type it themselves
    print(df.iloc[1:, 0])
    user = v.integer(f'Please enter the number of the user you would like to {_str}. ')
    user = f"volunteer{user}"
    df.loc[df['username'] == user, 'status'] = status  # modify the dataform
    df.to_csv('users.csv', index=False)  # write it into the .csv file

    print(f'Complete. {user} is now modified.'
          "All status below:")
    print(df)
