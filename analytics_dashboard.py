# analytics_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from models import TransactionModel
from utils import UIHelper
from datetime import datetime

class AnalyticsDashboard:
    def __init__(self, parent):
        self.parent = parent
        self.setup_analytics_tab()
    
    def setup_analytics_tab(self):
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Create main container
        main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#2c3e50', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📊 Library Analytics Dashboard", 
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)
        
        # Create notebook for different analytics views
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Most Issued Books
        self.create_most_issued_tab(notebook)
        
        # Tab 2: Monthly Trends
        self.create_monthly_trends_tab(notebook)
        
        # Tab 3: Member Activity
        self.create_member_activity_tab(notebook)
        
        # Tab 4: Data Tables
        self.create_data_tables_tab(notebook)
        
        # Refresh button
        refresh_btn = tk.Button(main_frame, text="🔄 Refresh Data", 
                               command=self.refresh_all,
                               bg='#3498db', fg='white', font=('Arial', 11),
                               cursor='hand2', width=20)
        refresh_btn.pack(pady=5)
    
    def create_most_issued_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="📚 Most Issued Books")
        
        # Control frame
        control_frame = tk.Frame(tab, bg='#ecf0f1', height=40)
        control_frame.pack(fill='x', padx=10, pady=5)
        control_frame.pack_propagate(False)
        
        tk.Label(control_frame, text="Top Books by Issue Count", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(side='left', padx=10, pady=5)
        
        # Create figure for matplotlib - FIXED: Use Figure instead of plt
        fig = Figure(figsize=(10, 5), dpi=100, facecolor='#f0f0f0')
        
        # Create subplots
        ax1 = fig.add_subplot(121)  # 1 row, 2 columns, position 1
        ax2 = fig.add_subplot(122)  # 1 row, 2 columns, position 2
        
        # Get data
        df = TransactionModel.get_transaction_stats()
        
        if not df.empty and len(df) > 0:
            # Prepare data for top 5
            top_5 = df.head(5)
            
            # Bar chart
            bars = ax1.bar(range(len(top_5)), top_5['Issue Count'], 
                          color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'])
            ax1.set_title('Top 5 Most Issued Books', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Book Title', fontsize=10)
            ax1.set_ylabel('Number of Issues', fontsize=10)
            ax1.set_xticks(range(len(top_5)))
            ax1.set_xticklabels([title[:20] + '...' if len(title) > 20 else title 
                                for title in top_5['Book Title']], rotation=45, ha='right', fontsize=8)
            
            # Add value labels on bars
            for i, (bar, count) in enumerate(zip(bars, top_5['Issue Count'])):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(count)}', ha='center', va='bottom', fontsize=9)
            
            # Pie chart
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
            wedges, texts, autotexts = ax2.pie(top_5['Issue Count'], 
                                               labels=top_5['Book Title'],
                                               autopct='%1.1f%%',
                                               colors=colors[:len(top_5)],
                                               startangle=90,
                                               textprops={'fontsize': 8})
            ax2.set_title('Issue Distribution', fontsize=12, fontweight='bold')
            
            # Improve pie chart labels
            for text in texts:
                text.set_fontsize(8)
            for autotext in autotexts:
                autotext.set_fontsize(8)
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        else:
            ax1.text(0.5, 0.5, 'No transaction data available', 
                    ha='center', va='center', transform=ax1.transAxes, fontsize=12)
            ax2.text(0.5, 0.5, 'No data', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=12)
        
        fig.tight_layout()
        
        # Embed in tkinter - FIXED: Proper canvas creation
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)
        
        # Statistics frame
        stats_frame = tk.Frame(tab, bg='white', relief='groove', bd=2)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        if not df.empty:
            total_issues = df['Issue Count'].sum()
            most_issued = df.iloc[0]['Book Title']
            most_issued_count = df.iloc[0]['Issue Count']
            
            tk.Label(stats_frame, text=f"📊 Total Issues: {total_issues}", 
                    font=('Arial', 11), bg='white').pack(side='left', padx=20, pady=8)
            tk.Label(stats_frame, text=f"🏆 Most Issued: '{most_issued[:30]}...' ({most_issued_count} times)", 
                    font=('Arial', 11), bg='white', fg='#27ae60').pack(side='left', padx=20, pady=8)
        else:
            tk.Label(stats_frame, text="No transaction data available", 
                    font=('Arial', 11), bg='white').pack(pady=8)
    
    def create_monthly_trends_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="📈 Monthly Trends")
        
        # Get data
        df = TransactionModel.get_monthly_stats()
        
        # Create figure - FIXED: Use Figure
        fig = Figure(figsize=(10, 5), dpi=100, facecolor='#f0f0f0')
        ax = fig.add_subplot(111)
        
        if not df.empty and len(df) > 0:
            # Line chart for monthly trends
            x = range(len(df))
            ax.plot(x, df['Issues'], marker='o', linewidth=2, markersize=8, 
                   color='#e74c3c', markerfacecolor='#c0392b', markeredgecolor='white')
            ax.fill_between(x, df['Issues'], alpha=0.2, color='#e74c3c')
            
            ax.set_title('Monthly Book Issues Trend', fontsize=14, fontweight='bold')
            ax.set_xlabel('Month', fontsize=11)
            ax.set_ylabel('Number of Issues', fontsize=11)
            ax.set_xticks(x)
            ax.set_xticklabels(df['Month'], rotation=45, ha='right')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Add value labels on points
            for i, (month, issues) in enumerate(zip(df['Month'], df['Issues'])):
                ax.annotate(str(issues), (i, issues), 
                           textcoords="offset points", xytext=(0,10), 
                           ha='center', fontsize=9, fontweight='bold')
            
            # Set y-axis to integer only
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        else:
            ax.text(0.5, 0.5, 'No monthly data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)
        
        # Summary
        summary_frame = tk.Frame(tab, bg='white', relief='groove', bd=2)
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        if not df.empty and len(df) > 0:
            avg_issues = df['Issues'].mean()
            max_idx = df['Issues'].idxmax()
            max_month = df.loc[max_idx, 'Month']
            max_issues = df.loc[max_idx, 'Issues']
            
            tk.Label(summary_frame, text=f"📊 Average Monthly Issues: {avg_issues:.1f}", 
                    font=('Arial', 11), bg='white').pack(side='left', padx=20, pady=8)
            tk.Label(summary_frame, text=f"📈 Peak Month: {max_month} ({max_issues} issues)", 
                    font=('Arial', 11), bg='white', fg='#27ae60').pack(side='left', padx=20, pady=8)
        else:
            tk.Label(summary_frame, text="No monthly data available", 
                    font=('Arial', 11), bg='white').pack(pady=8)
    
    def create_member_activity_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="👥 Member Activity")
        
        # Get data
        df = TransactionModel.get_member_activity()
        
        # Create figure - FIXED: Use Figure
        fig = Figure(figsize=(10, 5), dpi=100, facecolor='#f0f0f0')
        ax = fig.add_subplot(111)
        
        if not df.empty and len(df) > 0:
            # Horizontal bar chart for top members
            y_pos = range(len(df))
            bars = ax.barh(y_pos, df['Books Borrowed'], color='#3498db', height=0.6)
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels([name[:20] + '...' if len(name) > 20 else name 
                               for name in df['Member Name']])
            ax.set_xlabel('Number of Books Borrowed', fontsize=11)
            ax.set_title('Top 5 Most Active Members', fontsize=14, fontweight='bold')
            ax.invert_yaxis()  # Display top member at the top
            
            # Add value labels
            for i, (bar, count) in enumerate(zip(bars, df['Books Borrowed'])):
                ax.text(count + 0.1, bar.get_y() + bar.get_height()/2,
                       f'{int(count)}', va='center', fontsize=10, fontweight='bold')
            
            # Set x-axis to integer only
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        else:
            ax.text(0.5, 0.5, 'No member activity data', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)
        
        # Member list
        list_frame = tk.Frame(tab, bg='white', relief='groove', bd=2)
        list_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(list_frame, text="🏆 Top Members", font=('Arial', 12, 'bold'), 
                bg='white').pack(pady=5)
        
        if not df.empty and len(df) > 0:
            for idx, row in df.iterrows():
                member_text = f"{idx+1}. {row['Member Name']} (ID: {row['Member ID']}) - {row['Books Borrowed']} books"
                tk.Label(list_frame, text=member_text, font=('Arial', 10), 
                        bg='white', anchor='w').pack(padx=20, fill='x')
        else:
            tk.Label(list_frame, text="No member activity data", 
                    font=('Arial', 10), bg='white').pack(pady=5)
    
    def create_data_tables_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="📋 Data Tables")
        
        # Create notebook for different tables
        inner_notebook = ttk.Notebook(tab)
        inner_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Book Issues Table
        self.create_book_issues_table(inner_notebook)
        
        # Tab 2: Monthly Stats Table
        self.create_monthly_stats_table(inner_notebook)
        
        # Tab 3: Member Activity Table
        self.create_member_activity_table(inner_notebook)
    
    def create_book_issues_table(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Book Issues")
        
        # Create treeview with scrollbars
        tree_frame = tk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        tree = ttk.Treeview(tree_frame, 
                           columns=('Rank', 'Book Title', 'Book ID', 'Issue Count'), 
                           show='headings',
                           yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)
        
        # Configure headings
        tree.heading('Rank', text='Rank')
        tree.heading('Book Title', text='Book Title')
        tree.heading('Book ID', text='Book ID')
        tree.heading('Issue Count', text='Issue Count')
        
        # Configure columns
        tree.column('Rank', width=60, minwidth=50, anchor='center')
        tree.column('Book Title', width=300, minwidth=200)
        tree.column('Book ID', width=80, minwidth=70, anchor='center')
        tree.column('Issue Count', width=100, minwidth=80, anchor='center')
        
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load data
        df = TransactionModel.get_transaction_stats()
        if not df.empty:
            for idx, row in df.iterrows():
                tree.insert('', 'end', values=(idx+1, row['Book Title'], row['Book ID'], row['Issue Count']))
        
        # Export button
        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill='x', pady=5)
        
        export_btn = tk.Button(btn_frame, text="📥 Export to CSV", 
                              command=lambda: self.export_to_csv(df, 'book_issues.csv'),
                              bg='#27ae60', fg='white', font=('Arial', 10),
                              cursor='hand2', width=15)
        export_btn.pack()
    
    def create_monthly_stats_table(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Monthly Stats")
        
        tree_frame = tk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        tree = ttk.Treeview(tree_frame, 
                           columns=('Month', 'Issues'), 
                           show='headings',
                           yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)
        
        # Configure headings
        tree.heading('Month', text='Month')
        tree.heading('Issues', text='Number of Issues')
        
        # Configure columns
        tree.column('Month', width=150, minwidth=100, anchor='center')
        tree.column('Issues', width=150, minwidth=100, anchor='center')
        
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load data
        df = TransactionModel.get_monthly_stats()
        if not df.empty:
            for _, row in df.iterrows():
                tree.insert('', 'end', values=(row['Month'], row['Issues']))
        
        # Export button
        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill='x', pady=5)
        
        export_btn = tk.Button(btn_frame, text="📥 Export to CSV", 
                              command=lambda: self.export_to_csv(df, 'monthly_stats.csv'),
                              bg='#27ae60', fg='white', font=('Arial', 10),
                              cursor='hand2', width=15)
        export_btn.pack()
    
    def create_member_activity_table(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Member Activity")
        
        tree_frame = tk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        tree = ttk.Treeview(tree_frame, 
                           columns=('Rank', 'Member Name', 'Member ID', 'Books Borrowed'), 
                           show='headings',
                           yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)
        
        # Configure headings
        tree.heading('Rank', text='Rank')
        tree.heading('Member Name', text='Member Name')
        tree.heading('Member ID', text='Member ID')
        tree.heading('Books Borrowed', text='Books Borrowed')
        
        # Configure columns
        tree.column('Rank', width=60, minwidth=50, anchor='center')
        tree.column('Member Name', width=200, minwidth=150)
        tree.column('Member ID', width=100, minwidth=80, anchor='center')
        tree.column('Books Borrowed', width=120, minwidth=100, anchor='center')
        
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Load data
        df = TransactionModel.get_member_activity()
        if not df.empty:
            for idx, row in df.iterrows():
                tree.insert('', 'end', values=(idx+1, row['Member Name'], row['Member ID'], row['Books Borrowed']))
        
        # Export button
        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill='x', pady=5)
        
        export_btn = tk.Button(btn_frame, text="📥 Export to CSV", 
                              command=lambda: self.export_to_csv(df, 'member_activity.csv'),
                              bg='#27ae60', fg='white', font=('Arial', 10),
                              cursor='hand2', width=15)
        export_btn.pack()
    
    def export_to_csv(self, df, filename):
        """Export DataFrame to CSV"""
        if not df.empty:
            df.to_csv(filename, index=False)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        else:
            messagebox.showwarning("No Data", "No data to export")
    
    def refresh_all(self):
        """Refresh all analytics data"""
        self.setup_analytics_tab()
        messagebox.showinfo("Refresh", "Analytics data refreshed successfully!")