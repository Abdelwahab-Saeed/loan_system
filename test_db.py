from db import DatabaseManager  # Adjust this if in another file

db = DatabaseManager()
db.execute("SELECT version();")
print("PostgreSQL Version:", db.fetchone())
db.close()
