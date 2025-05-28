from db import DatabaseManager
from decimal import Decimal

class Payment:
    def __init__(self):
        self.db = DatabaseManager()

    def make_payment(self, loan_id: int, amount: float) -> bool:
        #This helped me to avoid doing arithmetic operation between float and decimal
        amount = Decimal(str(amount))
        if amount <= 0:
            print("Payment amount must be positive.")
            return False

        # Check loan remaining balance
        self.db.execute("SELECT remaining_balance, status FROM loans WHERE id = %s", (loan_id,))
        result = self.db.fetchone()
        if not result:
            print("Loan not found.")
            return False

        remaining_balance, status = result
        if status != 'active':
            print("Loan is not active. Cannot make payments.")
            return False

        if amount > remaining_balance:
            print(f"Payment exceeds remaining balance ({remaining_balance:.2f}).")
            return False

        # Insert payment record
        self.db.execute(
            "INSERT INTO payments (loan_id, amount) VALUES (%s, %s)",
            (loan_id, amount)
        )

        # Update loan remaining balance
        new_balance = remaining_balance - amount
        new_status = 'closed' if new_balance == 0 else 'active'
        self.db.execute(
            "UPDATE loans SET remaining_balance = %s, status = %s WHERE id = %s",
            (new_balance, new_status, loan_id)
        )

        print(f"Payment of {amount:.2f} made successfully. Remaining balance: {new_balance:.2f}")
        return True

    def get_payment_history(self, loan_id: int):
        self.db.execute(
            "SELECT id, amount, payment_date FROM payments WHERE loan_id = %s ORDER BY payment_date DESC",
            (loan_id,)
        )
        payments = self.db.fetchall()
        return payments

    def view_history(self, user_id: int):
        # Get all loans for the user
        self.db.execute("SELECT id FROM loans WHERE user_id = %s", (user_id,))
        loans = self.db.fetchall()

        if not loans:
            print("No loans found for this user.")
            return

        for loan in loans:
            loan_id = loan[0]
            print(f"\n--- Payment History for Loan ID: {loan_id} ---")
            payments = self.get_payment_history(loan_id)
            if not payments:
                print("No payments made yet.")
            else:
                for payment in payments:
                    payment_id, amount, date = payment
                    print(f"Payment ID: {payment_id}, Amount: {amount:.2f}, Date: {date}")

    def close(self):
        self.db.close()
