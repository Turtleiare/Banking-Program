import sqlite3
from getpass import getpass
from random import randint

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    account_number INTEGER PRIMARY KEY,
                    pin INTEGER,
                    balance REAL
                )''')
conn.commit()
#account number doesn't show for some unknown reason
def create_account():
    pin = getpass("Create a 4-digit pin: ")
    pin_confirm = getpass("Confirm pin: ")
    if pin != pin_confirm or len(pin) != 4:
        print("Pin mismatch or invalid length. Account creation failed.")
        return

    account_number = randint(1000, 9999)
    balance = 0.0
    cursor.execute('''INSERT INTO accounts (account_number, pin, balance)
                    VALUES (?, ?, ?)''', (account_number, pin, balance))
    conn.commit()
    print(f"Account created successfully! Your account number is: {account_number}")

def login():
    account_number = int(input("Enter account number: "))
    pin = getpass("Enter pin: ")
    cursor.execute('''SELECT * FROM accounts WHERE account_number=? AND pin=?''', (account_number, pin))
    account = cursor.fetchone()
    if account:
        print("Login successful!")
        return account_number
    else:
        print("Invalid account number or pin.")
        return None

def check_balance(account_number):
    cursor.execute('''SELECT balance FROM accounts WHERE account_number=?''', (account_number,))
    balance = cursor.fetchone()[0]
    print(f"Your current balance is: ${balance}")

def deposit(account_number):
    amount = float(input("Enter deposit amount: $"))
    cursor.execute('''UPDATE accounts SET balance=balance+? WHERE account_number=?''', (amount, account_number))
    conn.commit()
    print("Deposit successful!")

def withdraw(account_number):
    amount = float(input("Enter withdrawal amount: $"))
    cursor.execute('''SELECT balance FROM accounts WHERE account_number=?''', (account_number,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute('''UPDATE accounts SET balance=balance-? WHERE account_number=?''', (amount, account_number))
        conn.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient funds.")

def close_account(account_number):
    confirm = input("Are you sure you want to close your account? This action cannot be undone. (yes/no): ")
    if confirm.lower() == 'yes':
        cursor.execute('''DELETE FROM accounts WHERE account_number=?''', (account_number,))
        conn.commit()
        print("Account closed successfully.")
    else:
        print("Account closure cancelled.")

def main():
    while True:
        print("\n1. Create Account\n2. Login\n3. Check Balance\n4. Deposit\n5. Withdraw\n6. Close Account\n7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            account_number = login()
            if account_number:
                while True:
                    print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout")
                    option = input("Enter your choice: ")
                    if option == '1':
                        check_balance(account_number)
                    elif option == '2':
                        deposit(account_number)
                    elif option == '3':
                        withdraw(account_number)
                    elif option == '4':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            account_number = login()
            if account_number:
                check_balance(account_number)
        elif choice == '4':
            account_number = login()
            if account_number:
                deposit(account_number)
        elif choice == '5':
            account_number = login()
            if account_number:
                withdraw(account_number)
        elif choice == '6':
            account_number = login()
            if account_number:
                close_account(account_number)
        elif choice == '7':
            print("Thank you for using our banking application.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()