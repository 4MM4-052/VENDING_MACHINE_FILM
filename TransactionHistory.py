import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Thêm import cho Treeview
from PIL import Image, ImageTk
import sqlite3
import datetime
class TransactionHistory:
    def __init__(self):
        self.connection = sqlite3.connect('transactions.db')
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    ticket_name TEXT NOT NULL,
                    payment_method TEXT NOT NULL,
                    date_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def add_transaction(self, transaction):
        with self.connection:
            self.connection.execute('INSERT INTO transactions (ticket_name, payment_method) VALUES (?, ?)',
                                    (transaction['name'], transaction['payment_method']))

    def get_history(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT ticket_name, payment_method, date_time FROM transactions')
        rows = cursor.fetchall()
        # Chuyển đổi thời gian từ UTC sang giờ địa phương
        history = []
        for row in rows:
            ticket_name, payment_method, date_time_utc = row
            # Chuyển đổi thời gian UTC sang giờ địa phương
            date_time_local = datetime.datetime.strptime(date_time_utc, '%Y-%m-%d %H:%M:%S')
            date_time_local = date_time_local + datetime.timedelta(hours=7)  # Giả sử múi giờ là UTC+7
            history.append((ticket_name, payment_method, date_time_local.strftime('%d/%m/%Y %H:%M:%S')))
        return history

    def clear_all_transactions(self):
        with self.connection:
            self.connection.execute('DELETE FROM transactions')

    def close(self):
        self.connection.close()

