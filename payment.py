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

    def close(self):
        self.db.close()
