import getpass
from user import User
from loan import Loan
from payment import Payment

def main_menu(user_id, username):
    loan = Loan()
    payment = Payment()

    while True:
        print("\n--- Loan Application System ---")
        print(f"Logged in as: {username}")
        print("1. Apply for Loan")
        print("2. Check Outstanding Balance")
        print("3. View All Loans")
        print("4. Make a Payment")
        print("5. View Payment History")
        print("6. Logout")

        choice = input("Select an option: ")

        if choice == '1':
            amount = float(input("Enter loan amount: "))
            loan.apply_loan(user_id, amount)

        elif choice == '2':
            balance = loan.get_outstanding_balance(user_id)
            print(f"Your outstanding loan balance is: {balance:.2f}")

        elif choice == '3':
            loans = loan.get_loans(user_id)
            if loans:
                for l in loans:
                    print(f"Loan ID: {l[0]}, Amount: {l[1]}, Remaining: {l[2]}, Status: {l[3]}, Created: {l[4]}")
            else:
                print("No loans found.")

        elif choice == '4':
            loans = loan.get_loans(user_id)
            if not loans:
                print("No loans available to pay.")
                continue
            print("Your loans:")
            for l in loans:
                print(f"Loan ID: {l[0]}, Remaining: {l[2]:.2f}, Status: {l[3]}")
            try:
                loan_id = int(input("Enter Loan ID to make payment: "))
                amount = float(input("Enter payment amount: "))
                payment.make_payment(loan_id, amount)
            except ValueError:
                print("Invalid input.")

        elif choice == '5':
            try:
                loan_id = int(input("Enter Loan ID to view payment history: "))
                payments = payment.get_payment_history(loan_id)
                if payments:
                    for p in payments:
                        print(f"Payment ID: {p[0]}, Amount: {p[1]:.2f}, Date: {p[2]}")
                else:
                    print("No payments found.")
            except ValueError:
                print("Invalid input.")

        elif choice == '6':
            print("Logging out...")
            loan.close()
            payment.close()
            break

        else:
            print("Invalid option. Try again.")

def start():
    user = User()

    while True:
        print("\n--- Welcome to the Loan Application System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            user.register(username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            if user.login(username, password):
                # Fetch user id after login
                user.db.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_id = user.db.fetchone()[0]
                main_menu(user_id, username)
            else:
                print("Login failed.")

        elif choice == '3':
            print("Goodbye!")
            user.close()
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    start()
