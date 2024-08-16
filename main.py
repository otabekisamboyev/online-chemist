from bank_account import BankAccount
from registration import Registration
from chemist import Chemist
from cart import Cart
from database_setup import database, database_cursor


chemist = Chemist(database, database_cursor)
registration = Registration(database, database_cursor)
bank_account = BankAccount(database, database_cursor)
cart = Cart(database, database_cursor)


login = None
password = None
balance = None
have_not_account = True
is_working = False

# signing up and logging in
while have_not_account:
    print("Welcome to online chemist!")
    account = input("Do you have an account? (y/n) or (type 'exit' or 'e' to exit): ")
    if account == "y":
        login, password = registration.login_password()
        if registration.sign_in(login, password):
            have_not_account = False
            is_working = True
    elif account == "n":
        print("Alright, so create an account!")
        login, password, balance = registration.new_login_password()
        registration.sign_up(login, password, balance)
    elif account.lower() == 'exit' or account.lower() == 'e':
        have_not_account = False
    else:
        print("Wrong input. Try again!")

# ordering or modifying
while is_working:
    print(f"What do you want:\n"
          f"\t1) Order Medicine (type order or 1): \n"
          f"\t2) Bank balance (type balance or 2): \n"
          f"\t3) Exit (type exit or 3): ")
    action = input()
    if action.lower() == "order" or action == "1":
        chemist.report_med()
        print("Which medicine do you want to buy?")
        med_name = input("Med name: ")
        med_quantity = int(input("Med quantity: "))
        if chemist.is_quantity_sufficient(med_name, med_quantity):
            if bank_account.is_transaction_successful(med_name, med_quantity, login):
                cart.add_to_cart(med_name, med_quantity)
                cart.remove_bank_balance(login)
                chemist.remove_med(med_name, med_quantity)
            else:
                print("Your balance is insufficient.")
        else:
            print("Quantity is not sufficient.")
    elif action.lower() == "balance" or action == "2":
        bank_account.report_balance(login)
    elif action.lower() == "exit" or action == "3":
        cart.add_to_database(login)
        print("Your final cart")
        cart.report_cart(login)
        print("Have a nice day!")
        is_working = False
