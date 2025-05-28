from db import DatabaseManager  

class Loan:
    def __init__(self):
        self.db = DatabaseManager()

    def apply_loan(self, user_id: int, amount: float) -> bool:
        if amount <= 0:
            print("Loan amount must be positive.")
            return False

        # Insert new loan with full amount as remaining balance, status active
        query = """
        INSERT INTO loans (user_id, amount, remaining_balance, status)
        VALUES (%s, %s, %s, 'active')
        """
        self.db.execute(query, (user_id, amount, amount))
        print(f"Loan of {amount:.2f} applied successfully.")
        return True

    def get_loans(self, user_id: int):
        query = "SELECT id, amount, remaining_balance, status, created_at FROM loans WHERE user_id = %s"
        self.db.execute(query, (user_id,))
        loans = self.db.fetchall()
        return loans  # list of tuples

    def get_outstanding_balance(self, user_id: int) -> float:
        # Sum of remaining_balance of all active loans
        query = "SELECT COALESCE(SUM(remaining_balance), 0) FROM loans WHERE user_id = %s AND status = 'active'"
        self.db.execute(query, (user_id,))
        result = self.db.fetchone()
        return float(result[0]) if result else 0.0

    def check_balance(self, user_id: int):
        loans = self.get_loans(user_id)
        if not loans:
            print("You have no loans.")
            return

        print("\n--- Your Loans ---")
        for loan in loans:
            loan_id, amount, remaining, status, created_at = loan
            print(f"Loan ID: {loan_id}, Amount: {amount:.2f}, Remaining: {remaining:.2f}, Status: {status}, Created At: {created_at}")
        
        total = self.get_outstanding_balance(user_id)
        print(f"\nTotal Outstanding Balance: {total:.2f}")

    def close(self):
        self.db.close()
