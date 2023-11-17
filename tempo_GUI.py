import pandas as pd
import tkinter as tk
from tkinter import messagebox
import logging
from admin import Admin
from volunteer import Volunteer

logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    filemode='w',
                    format='%(module)s - %(levelname)s - %(message)s')


def main_menu():
    root = tk.Tk()
    root.title("Humanitarian Management System: Main Menu")
    root.geometry("400x250")

    label = tk.Label(root, text="Welcome to the Humanitarian Management System"
                                "\nPlease select your user type.")
    label.pack(pady=10)

    admin_button = tk.Button(root, text="Admin", command=lambda: login("Admin"))
    admin_button.pack()

    volunteer_button = tk.Button(root, text="Volunteer", command=volunteer_main_menu)
    volunteer_button.pack()

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=10)

    root.mainloop()


def login(user_type):
    root = tk.Tk()
    root.title(user_type + " Login")
    root.geometry("400x250")

    label = tk.Label(root, text=(user_type + " Login"))
    label.pack()
    username_entry = tk.Entry(root, text="Username")
    username_entry.pack()
    password_entry = tk.Entry(root, text="Password", show="*")
    password_entry.pack()

    if user_type == "Admin":
        login_button = tk.Button(root, text="Login",
                                 command=lambda: admin_login(username_entry.get(), password_entry.get()))
        login_button.pack()
    if user_type == "Volunteer":
        login_button = tk.Button(root, text="Login",
                                 command=lambda: volunteer_login(username_entry.get(), password_entry.get()))
        login_button.pack()

    back_button = tk.Button(root, text="Back", command=root.destroy)
    back_button.pack(pady=10)

    root.mainloop()


def admin_login(username, password):
    # check login details against users table
    users = pd.read_csv('users.csv', dtype={'password': str})

    select_user = users[(users['username'] == username) & (users['account_type'] == "admin")]
    if len(select_user.index) == 0:  # username not registered
        messagebox.showerror("Error", "Username not found. Please try again.")
        return
    if select_user.iloc[0]['password'] != password:  # password incorrect
        messagebox.showerror("Error", "Incorrect password. Please try again.")
        return

    messagebox.showinfo("Success", "Login successful!")
    logging.info("User logged in as: Admin")

    # create admin object
    admin = Admin(username, password)
    admin.admin_menu()


def volunteer_main_menu():
    root = tk.Tk()
    root.title("Volunteer Main Menu")
    root.geometry("400x250")

    label = tk.Label(root, text="Volunteer Main Menu")
    label.pack(pady=10)

    register_button = tk.Button(root, text="Register as Volunteer", command=volunteer_registration)
    register_button.pack()

    login_button = tk.Button(root, text="Volunteer Login", command=lambda: login("Volunteer"))
    login_button.pack()

    back_button = tk.Button(root, text="Back", command=root.destroy)
    back_button.pack(pady=10)

    root.mainloop()


def volunteer_registration():
    root = tk.Tk()
    root.title("Volunteer Registration")
    root.geometry("300x200")

    # volunteer registration GUI to be implemented

    root.mainloop()


def volunteer_login(username, password):
    # check login details against users table
    users = pd.read_csv('users.csv', dtype={'password': str})

    select_user = users[(users['username'] == username) & (users['account_type'] == "volunteer")]
    if len(select_user.index) == 0:  # username not registered
        messagebox.showerror("Error", "Username not found. Please try again.")
        return

    if select_user.iloc[0]['password'] != password:  # password incorrect
        messagebox.showerror("Error", "Incorrect password. Please try again.")
        return

    if select_user.iloc[0]['active'] == 0:  # user has been deactivated
        messagebox.showerror("Error", "Your account has been deactivated. Please contact the system administrator.")
        return

    messagebox.showinfo("Success", "Login successful!")
    logging.info("User logged in as: Volunteer")

    # Login successful, initialise volunteer object and go to volunteer menu
    select_user = select_user.replace({pd.NA: None})
    v = Volunteer(select_user.iloc[0]['username'], select_user.iloc[0]['password'],
                  select_user.iloc[0]['first_name'], select_user.iloc[0]['last_name'], select_user.iloc[0]['email'],
                  select_user.iloc[0]['phone_number'], select_user.iloc[0]['gender'],
                  select_user.iloc[0]['date_of_birth'], select_user.iloc[0]['plan_id'],
                  select_user.iloc[0]['camp_name'])
    v.volunteer_menu()


if __name__ == "__main__":
    main_menu()
