import getpass
from user import User
from loan import Loan
from payment import Payment
from decimal import Decimal
import re

user = User()
loan = Loan()
payment = Payment()

# Validation utilities
def is_valid_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,30}$', username))

def is_valid_password(password):
    return len(password.strip()) > 0

def get_valid_number(prompt, positive_only=True):
    while True:
        value = input(prompt).strip()
        try:
            num = float(value)
            if positive_only and num <= 0:
                raise ValueError
            return num
        except ValueError:
            print("Invalid number. Please enter a valid positive number.")

def get_valid_option(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print("Invalid option. Please choose from", ", ".join(options))


def main_menu(user_id, username):
    while True:
        print(f"\nWelcome, {username}!")
        print("1. Apply for a Loan")
        print("2. Make a Payment")
        print("3. Check Balance")
        print("4. View Payment History")
        print("5. Logout")

        choice = get_valid_option("Select an option: ", ['1', '2', '3', '4', '5'])

        if choice == '1':
            amount = get_valid_number("Enter loan amount: ")
            loan.apply_loan(user_id, amount)

        elif choice == '2':
            user_loans = loan.get_loans(user_id)
            if not user_loans:
                print("No active loans to make a payment on.")
                continue

            print("Your loans:")
            for l in user_loans:
                print(f"Loan ID: {l[0]}, Remaining: {l[1]}, Status: {l[2]}")

            loan_ids = [str(l[0]) for l in user_loans]
            loan_id = get_valid_option("Enter Loan ID to make payment: ", loan_ids)
            amount = get_valid_number("Enter payment amount: ")

            payment.make_payment(int(loan_id), amount)

        elif choice == '3':
            loan.check_balance(user_id)

        elif choice == '4':
            payment.view_history(user_id)

        elif choice == '5':
            print("Logging out...\n")
            break


def start():
    while True:
        print("--- Welcome to the Loan Application System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = get_valid_option("Select an option: ", ['1', '2', '3'])

        if choice == '1':
            username = input("Enter username: ").strip()
            if not is_valid_username(username):
                print("Username must be 3–30 characters, alphanumeric or underscore.")
                continue

            password = getpass.getpass("Enter password: ")
            if not is_valid_password(password):
                print("Password cannot be empty.")
                continue

            user.register(username, password)

        elif choice == '2':
            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")

            user_id = user.login(username, password)
            if user_id:
                main_menu(user_id, username)

        elif choice == '3':
            print("Thank you for using the Loan Application System.")
            break


if __name__ == "__main__":
    start()
