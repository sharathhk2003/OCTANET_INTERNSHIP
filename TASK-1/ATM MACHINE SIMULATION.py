# Created by SHARATH
# This Python program simulates an ATM machine with basic functionalities such as
# account balance inquiry, cash withdrawal, cash deposit, PIN change, and viewing transaction history.

import time

class Account:
    # Constructor for initializing an Account object with a user ID, PIN, and an optional balance.
    def __init__(self, user_id, pin, balance=0):
        """
        Initializes a new Account instance.
        :param user_id: The ID of the user.
        :param pin: The PIN for the account.
        :param balance: The starting balance of the account, default is 0.
        """
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []  # List to store transaction history.

    # Method to check if the provided PIN matches the account's PIN.
    def check_pin(self, pin):
        """
        Verifies if the provided PIN matches the account's PIN.
        :param pin: The PIN to be checked.
        :return: True if the PIN matches, else False.
        """
        return self.pin == pin

    # Method to allow the user to change their PIN.
    def change_pin(self, old_pin, new_pin):
        """
        Allows the user to change their PIN.
        :param old_pin: The current PIN of the account.
        :param new_pin: The new PIN to be set.
        :return: A message indicating whether the PIN change was successful or not.
        """
        if self.check_pin(old_pin):
            self.pin = new_pin
            return "PIN changed successfully."
        else:
            return "Incorrect current PIN."

    # Method to deposit a specified amount into the account.
    def deposit(self, amount):
        """
        Deposits a specified amount into the account.
        :param amount: The amount to deposit.
        :return: A confirmation message with the new balance.
        """
        self.balance += amount
        self.transactions.append(('Deposit', amount))  # Logs the deposit transaction.
        return f"Deposit successful. New balance: ${self.balance:.2f}"

    # Method to withdraw a specified amount from the account if sufficient balance is available.
    def withdraw(self, amount):
        """
        Withdraws a specified amount from the account if sufficient balance is available.
        :param amount: The amount to withdraw.
        :return: A message indicating the success or failure of the withdrawal and the new balance.
        """
        if amount > self.balance:
            return 'Insufficient balance'
        else:
            self.balance -= amount
            self.transactions.append(('Withdraw', amount))  # Logs the withdrawal transaction.
            return f"Withdrawal successful. New balance: ${self.balance:.2f}"

    # Method to return the transaction history of the account.
    def get_transaction_history(self):
        """
        Returns the transaction history of the account.
        :return: A formatted string of the transaction history or a message if no transactions are available.
        """
        if self.transactions:
            history = "\n".join([f"{t[0]}: ${t[1]:.2f}" for t in self.transactions])
            return f"Transaction History:\n{history}"
        else:
            return 'No transactions available'

    # Method to transfer a specified amount to another account if sufficient balance is available.
    def transfer(self, target_account, amount):
        """
        Transfers a specified amount to another account if sufficient balance is available.
        :param target_account: The account to which the money is to be transferred.
        :param amount: The amount to transfer.
        :return: A message indicating the success or failure of the transfer and the new balance.
        """
        if amount > self.balance:
            return 'Insufficient balance'
        else:
            self.withdraw(amount)
            target_account.deposit(amount)
            self.transactions.append(('Transfer', amount))  # Logs the transfer transaction.
            return f"Transfer successful. New balance: ${self.balance:.2f}"


class ATM:
    # Constructor for initializing an ATM instance with an empty dictionary of accounts.
    def __init__(self):
        """
        Initializes a new ATM instance.
        """
        self.accounts = {}  # Dictionary to store all accounts, keyed by user_id.

    # Method to create a new account and add it to the ATM's account dictionary.
    def create_account(self, user_id, pin, balance=0):
        """
        Creates a new account and adds it to the ATM's account dictionary.
        :param user_id: The ID for the new account.
        :param pin: The PIN for the new account.
        :param balance: The initial balance for the new account.
        """
        self.accounts[user_id] = Account(user_id, pin, balance)

    # Method to prompt the user for their user ID and PIN, and return the corresponding account if credentials are valid.
    def access_account(self):
        """
        Prompts the user for their user ID and PIN, and returns the corresponding account if credentials are valid.
        :return: The account object if access is granted, else None.
        """
        print("\n--- Account Access ---")
        user_id = input("Enter your User ID: ").strip()
        pin = input("Enter your PIN: ").strip()

        if user_id in self.accounts and self.accounts[user_id].check_pin(pin):
            print("Access Granted!")
            return self.accounts[user_id]
        else:
            print("Invalid User ID or PIN. Please try again.")
            return None

    # The main loop of the ATM simulation that handles user choices and directs them to appropriate account operations.
    def run(self):
        """
        The main loop of the ATM simulation. Handles user choices and directs to appropriate account operations.
        """
        while True:
            print("\n" + "=" * 30)
            print(" Welcome to the ATM Machine ")
            print("=" * 30)
            print("1. Access Account")
            print("2. Quit")
            choice = input("Choose an option: ").strip()

            if choice == '1':
                account = self.access_account()
                if account:
                    while True:
                        print("\n--- Account Menu ---")
                        print("1. View Transaction History")
                        print("2. Withdraw Cash")
                        print("3. Deposit Cash")
                        print("4. Transfer Funds")
                        print("5. Change PIN")
                        print("6. Quit")
                        operation = input("Choose an operation: ").strip()

                        if operation == '1':
                            print(account.get_transaction_history())
                        elif operation == '2':
                            amount = self.get_amount("withdraw")
                            print(account.withdraw(amount))
                        elif operation == '3':
                            amount = self.get_amount("deposit")
                            print(account.deposit(amount))
                        elif operation == '4':
                            target_id = input("Enter target User ID: ").strip()
                            if target_id in self.accounts:
                                amount = self.get_amount("transfer")
                                print(account.transfer(self.accounts[target_id], amount))
                            else:
                                print("Target account not found.")
                        elif operation == '5':
                            old_pin = input("Enter your current PIN: ").strip()
                            new_pin = input("Enter your new PIN: ").strip()
                            print(account.change_pin(old_pin, new_pin))
                        elif operation == '6':
                            print("Returning to main menu...")
                            time.sleep(1)
                            break
                        else:
                            print("Invalid operation. Please choose a valid option.")
                else:
                    print("Returning to main menu...")
                    time.sleep(1)
            elif choice == '2':
                print("Thank you for using our ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    # Static method to prompt the user to input a valid amount for the chosen action (withdraw, deposit, transfer).
    @staticmethod
    def get_amount(action):
        """
        Prompts the user to input a valid amount for the chosen action (withdraw, deposit, transfer).
        :param action: The action being performed (withdraw, deposit, transfer).
        :return: The valid amount entered by the user.
        """
        while True:
            try:
                amount = float(input(f"Enter amount to {action}: ").strip())
                if amount > 0:
                    return amount
                else:
                    print("Please enter a positive amount.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

# Create an ATM instance
atm = ATM()

# Create some sample accounts for testing purposes
atm.create_account('SHARATH', '1188', 1000)
atm.create_account('atmuser1', '1111', 1500)
atm.create_account('atmuser2', '1112', 500)
atm.create_account('atmuser3', '1113', 2000)

# Run the ATM interface
atm.run()
