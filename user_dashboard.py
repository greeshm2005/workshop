# user_dashboard.py
import tkinter as tk
from tkinter import ttk
from models import BookModel, TransactionModel
from utils import UIHelper
from datetime import date

class UserDashboard:
    def __init__(self, parent, member, on_logout):
        self.parent = parent
        self.member = member
        self.on_logout = on_logout
        self.setup_dashboard()
    
    def setup_dashboard(self):
        UIHelper.clear_frame(self.parent)
        
        # Create main container
        main_container = tk.Frame(self.parent)
        main_container.pack(fill='both', expand=True)
        
        # Header frame with logout button (FIXED: Now visible)
        header_frame = tk.Frame(main_container, bg='#3498db', height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        # Welcome message with member details
        welcome_text = f"Welcome, {self.member[1]}! (ID: {self.member[0]})"
        tk.Label(header_frame, text=welcome_text, 
                font=('Arial', 14, 'bold'), bg='#3498db', fg='white').pack(side='left', padx=20, pady=15)
        
        # Member contact info
        contact_text = f"Contact: {self.member[2]}"
        tk.Label(header_frame, text=contact_text,
                font=('Arial', 10), bg='#3498db', fg='white').pack(side='left', padx=20)
        
        # Logout button (NOW VISIBLE)
        logout_btn = tk.Button(header_frame, text="Logout", command=self.on_logout,
                              bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                              width=10, height=1, bd=0, cursor='hand2')
        logout_btn.pack(side='right', padx=20, pady=15)
        
        # Main content
        main_frame = tk.Frame(main_container, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Browse Books Tab
        self.create_user_browse_tab(notebook)
        
        # My Transactions Tab
        self.create_user_transactions_tab(notebook)
        
        # My Profile Tab
        self.create_user_profile_tab(notebook)
    
    def create_user_browse_tab(self, notebook):
        browse_tab = ttk.Frame(notebook)
        notebook.add(browse_tab, text="📚 Browse Books")
        
        # Search frame
        search_frame = tk.LabelFrame(browse_tab, text="Search Books", font=('Arial', 12))
        search_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(search_frame, text="Search by:").pack(side='left', padx=5)
        self.user_search_var = tk.StringVar(value="Title")
        tk.Radiobutton(search_frame, text="Title", variable=self.user_search_var, 
                      value="Title").pack(side='left', padx=5)
        tk.Radiobutton(search_frame, text="Author", variable=self.user_search_var, 
                      value="Author").pack(side='left', padx=5)
        
        self.user_search_entry = tk.Entry(search_frame, width=40)
        self.user_search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.user_search_books,
                 bg='#3498db', fg='white', cursor='hand2').pack(side='left', padx=5)
        tk.Button(search_frame, text="Show All", command=self.user_load_books,
                 bg='#2ecc71', fg='white', cursor='hand2').pack(side='left', padx=5)
        
        # Treeview for books
        tree_frame = tk.Frame(browse_tab)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.user_book_tree = ttk.Treeview(tree_frame, 
                                           columns=('ID', 'Title', 'Author'), 
                                           show='headings',
                                           yscrollcommand=v_scrollbar.set,
                                           xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.user_book_tree.yview)
        h_scrollbar.config(command=self.user_book_tree.xview)
        
        # Configure columns
        self.user_book_tree.heading('ID', text='Book ID')
        self.user_book_tree.heading('Title', text='Title')
        self.user_book_tree.heading('Author', text='Author')
        
        self.user_book_tree.column('ID', width=100, minwidth=80)
        self.user_book_tree.column('Title', width=300, minwidth=200)
        self.user_book_tree.column('Author', width=250, minwidth=150)
        
        # Grid layout
        self.user_book_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.user_load_books()
    
    def user_load_books(self):
        for row in self.user_book_tree.get_children():
            self.user_book_tree.delete(row)
        
        books = BookModel.get_all()
        for book in books:
            self.user_book_tree.insert('', 'end', values=(book[0], book[1], book[2]))
    
    def user_search_books(self):
        search_term = self.user_search_entry.get()
        search_by = self.user_search_var.get()
        
        if not search_term:
            self.user_load_books()
            return
        
        for row in self.user_book_tree.get_children():
            self.user_book_tree.delete(row)
        
        books = BookModel.search(search_term, search_by)
        for book in books:
            self.user_book_tree.insert('', 'end', values=(book[0], book[1], book[2]))
    
    def create_user_transactions_tab(self, notebook):
        trans_tab = ttk.Frame(notebook)
        notebook.add(trans_tab, text="📋 My Transactions")
        
        tk.Label(trans_tab, text="Your Borrowing History", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Summary stats
        stats_frame = tk.Frame(trans_tab, bg='#ecf0f1')
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        # Get transactions for stats
        transactions = TransactionModel.get_by_member(self.member[0])
        active_books = len([t for t in transactions if t[5] >= date.today()])
        overdue_books = len([t for t in transactions if t[5] < date.today()])
        
        tk.Label(stats_frame, text=f"Total Books Borrowed: {len(transactions)}", 
                font=('Arial', 11), bg='#ecf0f1').pack(side='left', padx=20, pady=10)
        tk.Label(stats_frame, text=f"Currently Reading: {active_books}", 
                font=('Arial', 11), bg='#ecf0f1', fg='#27ae60').pack(side='left', padx=20, pady=10)
        tk.Label(stats_frame, text=f"Overdue Books: {overdue_books}", 
                font=('Arial', 11), bg='#ecf0f1', fg='#e74c3c').pack(side='left', padx=20, pady=10)
        
        # Treeview for user's transactions
        tree_frame = tk.Frame(trans_tab)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.user_trans_tree = ttk.Treeview(tree_frame, 
                                            columns=('ID', 'Book ID', 'Librarian', 'Issued', 'Due', 'Status'), 
                                            show='headings',
                                            yscrollcommand=v_scrollbar.set,
                                            xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.user_trans_tree.yview)
        h_scrollbar.config(command=self.user_trans_tree.xview)
        
        # Configure columns
        self.user_trans_tree.heading('ID', text='Transaction ID')
        self.user_trans_tree.heading('Book ID', text='Book ID')
        self.user_trans_tree.heading('Librarian', text='Librarian ID')
        self.user_trans_tree.heading('Issued', text='Issue Date')
        self.user_trans_tree.heading('Due', text='Due Date')
        self.user_trans_tree.heading('Status', text='Status')
        
        column_widths = {'ID': 120, 'Book ID': 100, 'Librarian': 100, 
                        'Issued': 100, 'Due': 100, 'Status': 100}
        for col, width in column_widths.items():
            self.user_trans_tree.column(col, width=width, minwidth=80)
        
        # Grid layout
        self.user_trans_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.load_user_transactions()
    
    def load_user_transactions(self):
        for row in self.user_trans_tree.get_children():
            self.user_trans_tree.delete(row)
        
        transactions = TransactionModel.get_by_member(self.member[0])
        
        for trans in transactions:
            # Determine status
            if trans[5] < date.today():
                status = "⚠️ Overdue"
                tags = ('overdue',)
            else:
                status = "✅ Active"
                tags = ('active',)
            
            item = self.user_trans_tree.insert('', 'end', values=(
                trans[0], trans[1], trans[3], trans[4], trans[5], status
            ), tags=tags)
        
        # Color coding
        self.user_trans_tree.tag_configure('overdue', background='#ffcccc')
        self.user_trans_tree.tag_configure('active', background='#ccffcc')
    
    def create_user_profile_tab(self, notebook):
        profile_tab = ttk.Frame(notebook)
        notebook.add(profile_tab, text="👤 My Profile")
        
        # Profile card
        card_frame = tk.LabelFrame(profile_tab, text="Member Information", 
                                   font=('Arial', 14, 'bold'), padx=20, pady=20)
        card_frame.pack(pady=30, padx=50, fill='both', expand=True)
        
        # Member details
        transactions = TransactionModel.get_by_member(self.member[0])
        details = [
            ("Member ID:", str(self.member[0])),
            ("Full Name:", self.member[1]),
            ("Contact Number:", self.member[2]),
            ("Member Since:", "2024"),
            ("Total Books Borrowed:", str(len(transactions))),
        ]
        
        for i, (label, value) in enumerate(details):
            tk.Label(card_frame, text=label, font=('Arial', 12, 'bold'),
                    anchor='e').grid(row=i, column=0, padx=10, pady=8, sticky='e')
            tk.Label(card_frame, text=value, font=('Arial', 12),
                    anchor='w').grid(row=i, column=1, padx=10, pady=8, sticky='w')
        
        # Library rules
        rules_frame = tk.LabelFrame(profile_tab, text="Library Rules", font=('Arial', 12))
        rules_frame.pack(pady=20, padx=50, fill='x')
        
        rules = [
            "• Books can be borrowed for 14 days",
            "• Late return fine: ₹10 per day",
            "• Maximum 3 books can be borrowed at a time",
            "• Lost books must be reported immediately",
            "• Handle books with care"
        ]
        
        for rule in rules:
            tk.Label(rules_frame, text=rule, font=('Arial', 10),
                    anchor='w').pack(padx=20, pady=2, fill='x')