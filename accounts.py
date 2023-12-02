from PyQt6.QtWidgets import *
from gui import *
import csv

class Accounts(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__account_name = 'john'
        self.__account_balance = 0

        self.set_balance_button.clicked.connect(lambda : self.set_balance())
        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)
        self.set_name_btn.clicked.connect(self.set_name)

        self.regular_account_button.clicked.connect(lambda: self.switch_page(0))
        self.saving_account_button.clicked.connect(lambda: self.switch_page(1))
        self.change_account_btn.clicked.connect(lambda: self.switch_page(2))

        self.warning_lbl.setText('')

    def load_data(self, name, balance) -> None:
        """
        takes the data given from the csv file for an account and uploads it to account balance and name
        :param name: name of the account
        :param balance: balance of the account
        :return: none
        """
        self.__account_balance = float(balance)
        self.__account_name = name
        self.account_name_lbl.setText(self.__account_name)


    def set_name(self) -> None:
        """
        takes the user input from entry and finds account with matching name
        if none then account is created with 0 set for balance
        :return: none
        """
        name = str(self.account_name_lnedit.text())
        self.account_name_lnedit.clear()

        try:
            with open('accounts.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for line in csv_reader:
                    if line[0] == name:
                        self.load_data(line[0], line[1])
                        return  # Account found, no need to proceed further

            # If the account is not found, append it to the end of the file
            with open('accounts.csv', 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                new_data = [name, 0]
                csv_writer.writerow(new_data)

        except FileNotFoundError:
            # If the file doesn't exist, create it and add the new account
            with open('accounts.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                new_data = [name, 0]
                csv_writer.writerow(new_data)

        self.display_balance()

    def switch_page(self, index) -> None:
        """
        function changes which of the stacked widget pages gets displayed
        :param index: the index of the page to switch to
        :return: none
        """
        self.stackedWidget.setCurrentIndex(index)
        self.display_balance()

    def display_balance(self) -> None:
        """
        function updates the balance to display
        :return: none
        """
        self.balance_label.setText(f'Balance: ${self.get_balance()}')
        self.warning_lbl.setText('')

    def save_account(self) -> None:
        """
        uploads the current name and balance data to the csv file with matching account name
        :return: none
        """
        accounts = []
        with open('accounts.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            accounts = list(csv_reader)

        for line in accounts:
            if line and line[0] == self.__account_name:
                line[1] = str(self.__account_balance)  # Assuming account_balance is a numerical value

        with open('accounts.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(accounts)

    def change_balance(self, value=0.0) -> None:
        """
        function will change the current balance to given value
        :param value: the value to change the current balance to
        :return: none
        """
        try:
            value = float(value)
        except ValueError:
            value = 0

        self.user_entry.clear()

        if value > 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0

        self.display_balance()


    def set_balance(self) -> None:
        """
        sets the current balance to value in user input field
        :return: none
        """
        try:
            value = float(self.user_entry.text())
        except ValueError:
            self.warning_lbl.setText(f'Can not accept value')
            return

        self.user_entry.clear()

        if value > 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0
        self.save_account()
        self.display_balance()

    def get_balance(self) -> float:
        """
        returns the current account balance from the accounts csv file
        :return: float
        """
        with open('accounts.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[0] == self.__account_name:
                    value = line[1]


        return float(value)


    def deposit(self) -> None:
        """
        adds the value from user entry filed to current balance
        :return: none
        """
        try:
            amount = float(self.user_entry.text())
        except ValueError:
            self.warning_lbl.setText(f'Can not accept value')
            return

        self.user_entry.clear()
        if amount > 0:
            self.change_balance(self.get_balance() + amount)

        self.save_account()
        self.display_balance()

    def withdraw(self):
        """
        subtracts the value from user entry field from current balance
        :return: none
        """
        try:
            amount = float(self.user_entry.text())
        except ValueError:
            self.warning_lbl.setText(f'Can not accept value')
            return -1

        self.user_entry.clear()

        if amount > 0:
            self.change_balance(self.get_balance() - amount)

        self.save_account()
        self.display_balance()


