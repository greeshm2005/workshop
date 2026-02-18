# models.py
from database import Database
from datetime import date, timedelta
import pandas as pd

class BookModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Book")
    
    @staticmethod
    def get_by_id(book_id):
        db = Database()
        return db.fetch_one("SELECT * FROM Book WHERE book_id = %s", (book_id,))
    
    @staticmethod
    def search(search_term, search_by="Title"):
        db = Database()
        if search_by == "Title":
            return db.fetch_all("SELECT * FROM Book WHERE title LIKE %s", (f"%{search_term}%",))
        else:
            return db.fetch_all("SELECT * FROM Book WHERE author LIKE %s", (f"%{search_term}%",))
    
    @staticmethod
    def add(book_id, title, author, librarian_id):
        db = Database()
        return db.execute_query(
            "INSERT INTO Book VALUES (%s, %s, %s, %s)",
            (book_id, title, author, librarian_id)
        )
    
    @staticmethod
    def update(book_id, title, author, librarian_id):
        db = Database()
        return db.execute_query(
            "UPDATE Book SET title=%s, author=%s, librarian_id=%s WHERE book_id=%s",
            (title, author, librarian_id, book_id)
        )
    
    @staticmethod
    def delete(book_id):
        db = Database()
        return db.execute_query("DELETE FROM Book WHERE book_id=%s", (book_id,))

class TransactionModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Transactions")
    
    @staticmethod
    def get_by_member(member_id):
        db = Database()
        return db.fetch_all("SELECT * FROM Transactions WHERE member_id = %s", (member_id,))
    
    @staticmethod
    def issue(trans_id, book_id, member_id, librarian_id):
        db = Database()
        issue_date = date.today()
        due_date = issue_date + timedelta(days=14)
        return db.execute_query(
            "INSERT INTO Transactions VALUES (%s, %s, %s, %s, %s, %s)",
            (trans_id, book_id, member_id, librarian_id, issue_date, due_date)
        )
    
    @staticmethod
    def return_book(trans_id):
        db = Database()
        return db.execute_query("DELETE FROM Transactions WHERE transaction_id=%s", (trans_id,))
    
    @staticmethod
    def get_overdue():
        db = Database()
        today = date.today()
        return db.fetch_all("SELECT * FROM Transactions WHERE due_date < %s", (today,))
    
    @staticmethod
    def get_transaction_stats():
        """Get transaction statistics using pandas"""
        db = Database()
        query = """
        SELECT 
            b.title,
            b.book_id,
            COUNT(t.transaction_id) as issue_count
        FROM Book b
        LEFT JOIN Transactions t ON b.book_id = t.book_id
        GROUP BY b.book_id, b.title
        ORDER BY issue_count DESC
        """
        data = db.fetch_all(query)
        
        if data and len(data) > 0:
            # Create pandas DataFrame
            df = pd.DataFrame(data, columns=['Book Title', 'Book ID', 'Issue Count'])
            return df
        return pd.DataFrame(columns=['Book Title', 'Book ID', 'Issue Count'])
    
    @staticmethod
    def get_monthly_stats():
        """Get monthly transaction statistics"""
        db = Database()
        # For MySQL
        query = """
        SELECT 
            DATE_FORMAT(date_issued, '%Y-%m') as month,
            COUNT(*) as issue_count
        FROM Transactions
        GROUP BY DATE_FORMAT(date_issued, '%Y-%m')
        ORDER BY month DESC
        LIMIT 6
        """
        
        data = db.fetch_all(query)
        
        if data and len(data) > 0:
            df = pd.DataFrame(data, columns=['Month', 'Issues'])
            # Reverse to show chronological order
            df = df.iloc[::-1].reset_index(drop=True)
            return df
        return pd.DataFrame(columns=['Month', 'Issues'])
    
    @staticmethod
    def get_member_activity():
        """Get most active members"""
        db = Database()
        query = """
        SELECT 
            m.name,
            m.member_id,
            COUNT(t.transaction_id) as borrow_count
        FROM Members m
        LEFT JOIN Transactions t ON m.member_id = t.member_id
        GROUP BY m.member_id, m.name
        ORDER BY borrow_count DESC
        LIMIT 5
        """
        data = db.fetch_all(query)
        
        if data and len(data) > 0:
            df = pd.DataFrame(data, columns=['Member Name', 'Member ID', 'Books Borrowed'])
            return df
        return pd.DataFrame(columns=['Member Name', 'Member ID', 'Books Borrowed'])

class LibrarianModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Librarian")
    
    @staticmethod
    def get_by_id(librarian_id):
        db = Database()
        return db.fetch_one("SELECT * FROM Librarian WHERE librarian_id = %s", (librarian_id,))

class MemberModel:
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Members")
    
    @staticmethod
    def get_by_id(member_id):
        db = Database()
        return db.fetch_one("SELECT * FROM Members WHERE member_id = %s", (member_id,))
    
    @staticmethod
    def validate_login(member_id, name):
        db = Database()
        return db.fetch_one(
            "SELECT * FROM Members WHERE member_id = %s AND name = %s",
            (member_id, name)
        )
    
    @staticmethod
    def register(member_id, name, contact):
        """Register a new member"""
        db = Database()
        # Check if member_id already exists
        existing = db.fetch_one("SELECT * FROM Members WHERE member_id = %s", (member_id,))
        if existing:
            return False, "Member ID already exists"
        
        # Insert new member
        success = db.execute_query(
            "INSERT INTO Members (member_id, name, contact) VALUES (%s, %s, %s)",
            (member_id, name, contact)
        )
        if success:
            return True, "Member registered successfully"
        else:
            return False, "Registration failed"
    
    @staticmethod
    def get_next_member_id():
        """Get the next available member ID"""
        db = Database()
        result = db.fetch_one("SELECT MAX(member_id) FROM Members")
        if result and result[0]:
            return result[0] + 1
        else:
            return 201  # Starting ID if no members exist

# FIXED: Added AdminModel class
class AdminModel:
    @staticmethod
    def validate_login(username, password):
        db = Database()
        return db.fetch_one(
            "SELECT * FROM Admin WHERE username = %s AND password = %s",
            (username, password)
        )
    
    @staticmethod
    def get_all():
        db = Database()
        return db.fetch_all("SELECT * FROM Admin")
    
    @staticmethod
    def add_admin(username, password, name, email):
        db = Database()
        return db.execute_query(
            "INSERT INTO Admin (username, password, name, email) VALUES (%s, %s, %s, %s)",
            (username, password, name, email)
        )