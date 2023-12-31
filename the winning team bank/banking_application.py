# imports

from tkinter import *

from tkinter import ttk

import os

from PIL import ImageTk, Image

from fpdf import FPDF

import datetime  # Added import for datetime


# Main Screen

master = Tk()

master.title('Banking App')

# Load and display the image

img = Image.open("the winning team.jpg")  # Replace "bank_image.jpg" with the actual path to your image

img = img.resize((250, 250))  # Resize the image if needed

img = ImageTk.PhotoImage(img)

img_label = Label(master, image=img)

img_label.grid(row=2, sticky=N, pady=10)

# Functions

def finish_reg():
    name = temp_name.get()

    age = temp_age.get()

    gender = temp_gender.get()

    password = temp_password.get()

    all_accounts = os.listdir()

    if name == "" or age == "" or gender == "" or password == "":
        notif.config(fg="red", text="All fields required * ")

        return

    for name_check in all_accounts:

        if name == name_check:

            notif.config(fg="red",

                         text="Account already exists")

            return

        else:

            new_file = open(name, "w")

            new_file.write(name + '\n')

            new_file.write(password + '\n')

            new_file.write(age + '\n')

            new_file.write(gender + '\n')

            new_file.write('0')

            new_file.close()

            notif.config(fg="green",

                         text="Account has been created")


def register():
    # Vars

    global temp_name

    global temp_age

    global temp_gender

    global temp_password

    global notif

    temp_name = StringVar()

    temp_age = StringVar()

    temp_gender = StringVar()

    temp_password = StringVar()

    # Register Screen

    register_screen = Toplevel(master)

    register_screen.title('Register')

    # Labels

    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12)).grid(row=0,
                                                                                                          sticky=N,
                                                                                                          pady=10)

    Label(register_screen, text="Name", font=('Calibri', 12)).grid(row=1, sticky=W)

    Label(register_screen, text="Age", font=('Calibri', 12)).grid(row=2, sticky=W)

    Label(register_screen, text="Gender", font=('Calibri', 12)).grid(row=3, sticky=W)

    Label(register_screen, text="Password:", font=('Calibri', 12)).grid(row=4, sticky=W)

    notif = Label(register_screen, font=('Calibri', 12))

    notif.grid(row=6, sticky=N, pady=10)

    # Entries

    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0)

    Entry(register_screen, textvariable=temp_age).grid(row=2, column=0)

    Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0)

    Entry(register_screen, textvariable=temp_password, show="*").grid(row=4, column=0)

    # Buttons

    Button(register_screen, text="Register", command=finish_reg, font=('Calibri', 12)).grid(row=7, sticky=N, pady=10)


def login_session():
    global login_name

    all_accounts = os.listdir()

    login_name = temp_login_name.get()

    login_password = temp_login_password.get()

    for name in all_accounts:

        if name == login_name:

            file = open(name, "r")

            file_data = file.read()

            file_data = file_data.split('\n')

            password = file_data[1]

            # Account Dashboard

            if login_password == password:

                login_screen.destroy()

                account_dashboard = Toplevel(master)

                account_dashboard.title('Dashboard')

                # Labels

                Label(account_dashboard, text="Account Dashboard", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

                Label(account_dashboard, text="Welcome " + name, font=('Calibri', 12)).grid(row=1, sticky=N, pady=5)

                # Buttons

                Button(account_dashboard, text="Personal Details", font=('Calibri', 12), width=30,
                       command=personal_details).grid(row=2, sticky=N, padx=10)

                Button(account_dashboard, text="Deposit", font=('Calibri', 12), width=30, command=deposit).grid(row=3,
                                                                                                                sticky=N,
                                                                                                                padx=10,
                                                                                                                pady=5)

                Button(account_dashboard, text="Withdraw", font=('Calibri', 12), width=30, command=withdraw).grid(row=4,
                                                                                                                  sticky=N,
                                                                                                                  padx=10,
                                                                                                                  pady=5)

                # Button(account_dashboard, text="Withdraw",font=('Calibri',12),width=30,command=withdraw).grid(row=4, column=1,sticky=N,padx=10)

                Button(account_dashboard, text="Balance", font=('Calibri', 12), width=30, command=view_balance).grid(
                    row=5, sticky=N, padx=10, pady=5)

                Button(account_dashboard, text="Statement", font=('Calibri', 12), width=30,
                       command=view_statement).grid(row=6, sticky=N, padx=10)

                Label(account_dashboard).grid(row=7, sticky=N, pady=10)

                return

            else:

                login_notif.config(fg="red", text="Password incorrect!!")

                return

    login_notif.config(fg="red", text="No account found !!")


def deposit():
    # Vars

    global amount

    global deposit_notif

    global current_balance_label

    amount = StringVar()

    file = open(login_name, "r")

    file_data = file.read()

    user_details = file_data.split('\n')

    details_balance = user_details[4]

    # Deposit Screen

    deposit_screen = Toplevel(master)

    deposit_screen.title('Deposit')

    # Label

    Label(deposit_screen, text="Deposit", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

    current_balance_label = Label(deposit_screen, text="Current Balance : R" + details_balance, font=('Calibri', 12))

    current_balance_label.grid(row=1, sticky=W)

    Label(deposit_screen, text="Amount : ", font=('Calibri', 12)).grid(row=2, sticky=W)

    deposit_notif = Label(deposit_screen, font=('Calibri', 12))

    deposit_notif.grid(row=4, sticky=N, pady=5)

    # Entry

    Entry(deposit_screen, textvariable=amount).grid(row=2, column=1)

    # Button

    Button(deposit_screen, text="Finish", font=('Calibri', 12), command=finish_deposit).grid(row=3, sticky=W, pady=5)


def finish_deposit():
    if amount.get() == "":
        deposit_notif.config(text='Amount is required!', fg="red")

        return

    if float(amount.get()) <= 0:
        deposit_notif.config(text='Negative currency is not accepted', fg='red')

        return

    file = open(login_name, 'r+')

    file_data = file.read()

    details = file_data.split('\n')

    current_balance = details[4]

    updated_balance = current_balance

    updated_balance = float(updated_balance) + float(amount.get())

    file_data = file_data.replace(current_balance, str(updated_balance))

    file_data += '\nDeposit: R' + amount.get()

    file.seek(0)

    file.truncate(0)

    file.write(file_data)

    file.close()

    current_balance_label.config(text="Current Balance : R" + str(updated_balance), fg="green")

    deposit_notif.config(text='Balance Updated', fg='green')


def withdraw():
    # Vars

    global withdraw_amount

    global withdraw_notif

    global current_balance_label

    withdraw_amount = StringVar()

    file = open(login_name, "r")

    file_data = file.read()

    user_details = file_data.split('\n')

    details_balance = user_details[4]

    file_data += '\nWithdraw: R' + withdraw_amount.get()

    # Deposit Screen

    withdraw_screen = Toplevel(master)

    withdraw_screen.title('Withdraw')

    # Label

    Label(withdraw_screen, text="Deposit", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

    current_balance_label = Label(withdraw_screen, text="Current Balance : R" + details_balance, font=('Calibri', 12))

    current_balance_label.grid(row=1, sticky=W)

    Label(withdraw_screen, text="Amount : ", font=('Calibri', 12)).grid(row=2, sticky=W)

    withdraw_notif = Label(withdraw_screen, font=('Calibri', 12))

    withdraw_notif.grid(row=4, sticky=N, pady=5)

    # Entry

    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2, column=1)

    # Button

    Button(withdraw_screen, text="Finish", font=('Calibri', 12), command=finish_withdraw).grid(row=3, sticky=W, pady=5)


def view_balance():
    file = open(login_name, 'r')

    file_data = file.read()

    user_details = file_data.split('\n')

    balance = user_details[4]

    file.close()

    balance_screen = Toplevel(master)

    balance_screen.title('Balance')

    Label(balance_screen, text="Your current balance is: R " + balance, font=('Calibri', 12)).pack()


def view_statement():
    file_name = login_name + "Transaction_statement.pdf"

    pdf = FPDF()

    pdf.set_font("Arial", size=12)

    pdf.add_page()

    file = open(login_name, 'r')

    file_data = file.read()

    details = file_data.split('\n')

    if len(details) > 5:

        transactions = details[5:]  # Get the transaction history

        transactions = [transaction for transaction in transactions if transaction.strip()]  # Remove empty transactions

        pdf.cell(0, 10, "Transaction Statement", ln=True)

        pdf.cell(0, 10, "----------------------------------", ln=True)

        for transaction in transactions:

            if transaction.startswith("Deposit"):

                pdf.cell(0, 10, "Credited amount     : + " + transaction[8:] + " ",
                         ln=True)  # Add each deposit transaction to the PDF file

            elif transaction.startswith("Withdraw"):

                pdf.cell(0, 10, "Debited amount   : - " + transaction[9:] + " ",
                         ln=True)  # Add each withdrawal transaction to the PDF file

        pdf.output(file_name)

        file.close()

        os.system(file_name)

    else:

        print("No transaction history available.")


def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(text='Amount is required!', fg="red")

        return

    if float(withdraw_amount.get()) <= 0:
        withdraw_notif.config(text='Negative currency is not accepted', fg='red')

        return

    file = open(login_name, 'r+')

    file_data = file.read()

    details = file_data.split('\n')

    current_balance = details[4]

    if float(withdraw_amount.get()) > float(current_balance):
        withdraw_notif.config(text='Insufficient Funds!', fg='red')

        return

    updated_balance = float(current_balance) - float(withdraw_amount.get())

    file_data = file_data.replace(current_balance, str(updated_balance))

    file_data += '\nWithdraw: R' + withdraw_amount.get()  # Append withdrawal transaction to file

    file.seek(0)

    file.truncate(0)

    file.write(file_data)

    file.close()

    current_balance_label.config(text="Current Balance : R" + str(updated_balance), fg="green")

    withdraw_notif.config(text='Balance Updated', fg='green')


def personal_details():
    # Vars

    file = open(login_name, 'r')

    file_data = file.read()

    user_details = file_data.split('\n')

    details_name = user_details[0]

    details_age = user_details[2]

    details_gender = user_details[3]

    details_balance = user_details[4]

    # Personal details screen

    personal_details_screen = Toplevel(master)

    personal_details_screen.title('Personal Details')

    # Labels

    Label(personal_details_screen, text="Personal Details", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

    Label(personal_details_screen, text="Name : " + details_name, font=('Calibri', 12)).grid(row=1, sticky=W)

    Label(personal_details_screen, text="Age : " + details_age, font=('Calibri', 12)).grid(row=2, sticky=W)

    Label(personal_details_screen, text="Gender : " + details_gender, font=('Calibri', 12)).grid(row=3, sticky=W)

    Label(personal_details_screen, text="Balance :R" + details_balance, font=('Calibri', 12)).grid(row=4, sticky=W)


def login():
    # Vars

    global temp_login_name

    global temp_login_password

    global login_notif

    global login_screen

    temp_login_name = StringVar()

    temp_login_password = StringVar()

    # Login Screen

    login_screen = Toplevel(master)

    login_screen.title('Login')

    # Labels

    Label(login_screen, text="Login to your account", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

    Label(login_screen, text="Username:", font=('Calibri', 12)).grid(row=1, sticky=W)

    Label(login_screen, text="Password:", font=('Calibri', 12)).grid(row=2, sticky=W)

    login_notif = Label(login_screen, font=('Calibri', 12))

    login_notif.grid(row=4, sticky=N)

    # Entry

    Entry(login_screen, textvariable=temp_login_name).grid(row=1, column=1, padx=5)

    Entry(login_screen, textvariable=temp_login_password, show="*").grid(row=2, column=1, padx=5)

    # Button

    Button(login_screen, text="Login", command=login_session, width=15, font=('Calibri', 12)).grid(row=3, column=1,
                                                                                                   sticky=W, pady=5,
                                                                                                   padx=5)




# Labels

Label(master, text="THE WINNING TEAM BANK", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)

Label(master, text="Today, tomorrow, together", font=('Calibri', 12)).grid(row=1, sticky=N)



# Buttons

Button(master, text="Register", font=('Calibri', 12), width=20, command=register).grid(row=3, sticky=N)

Button(master, text="Login", font=('Calibri', 12), width=20, command=login).grid(row=4, sticky=N, pady=10)

master.mainloop()
 

    