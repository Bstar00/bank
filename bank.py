#!/usr/bin/python3

# Import required libraries
import sqlite3
from getpass import getpass
from datetime import datetime

# Connect to the database
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create necessary database tables if they don't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        email TEXT,
        balance REAL DEFAULT 0
    )
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
)

# Login or Register
def login_or_register():
    print("1. Login")
    print("2. Register")
    choice = input("Enter your choice: ")

    if choice == "1":
        login()
    elif choice == "2":
        register()
    else:
        print("Invalid choice!")
        login_or_register()

# Login
def login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    # Check if user exists and password is correct
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and user[2] == password:
        print(f"Welcome, {user[3]}!")
        show_menu(user)
    else:
        print("Invalid username or password!")
        login_or_register()

# Register
def register():
    username = input("Choose a username: ")
    password = getpass("Choose a password: ")
    full_name = input("Enter your full name: ")
    email = input("Enter your email address: ")

    # Insert new user into the database
    cursor.execute(
        "INSERT INTO users (username, password, full_name, email) VALUES (?, ?, ?, ?)",
        (username, password, full_name, email),
    )
    conn.commit()
    print("Registration successful. Please login.")
    login()

# Show main menu
def show_menu(user):
    print("\n--- Main Menu ---")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Logout")
    choice = input("Enter your choice: ")

    if choice == "1":
        check_balance(user)
    elif choice == "2":
        deposit(user)
    elif choice == "3":
        withdraw(user)
    elif choice == "4":
        logout()
    else:
        print("Invalid choice!")
        show_menu(user)

# Check account balance
def check_balance(user):
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user[0],))
    balance = cursor.fetchone()[0]
    print(f"Your current balance is: ${balance}")
    show_menu(user)

# Deposit funds
def deposit(user):
    amount = float(input("Enter the amount to deposit: "))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user[0]))
    cursor.execute(
        "INSERT INTO transactions (user_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
        (user[0], "Deposit", amount, datetime.now()),
    )
    conn.commit()
    print("Deposit successful!")
    show_menu(user)

# Withdraw funds
def withdraw(user):
    amount = float(input("Enter the amount to withdraw: "))
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user[0],))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user[0]))
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
            (user[0], "Withdrawal", amount, datetime.now()),
        )
        conn.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient funds!")

    show_menu(user)

# Logout
def logout():
    print("Logged out successfully.")
    login_or_register()

# Main program execution
if __name__ == "__main__":
    print("--- Bank Application ---")
    login_or_register()

    # Close database connection
    conn.close()
