from PyQt6.QtWidgets import *
from gui import *
import csv


class Accounts(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__account_name = 'nil'
        self.__account_balance = 0
        self.__MINIMUM = 100
        self.__RATE = 1.02
        self.__deposit_count = '0'

        self.set_balance_button.clicked.connect(lambda: self.set_balance())
        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)
        self.set_name_btn.clicked.connect(self.set_name)
        self.savings_deposit_btn.clicked.connect(self.deposit_savings)

        self.regular_account_button.clicked.connect(lambda: self.switch_page(0))
        self.saving_account_button.clicked.connect(lambda: self.switch_page(1))
        self.change_account_btn.clicked.connect(lambda: self.switch_page(2))

        self.warning_lbl.setText('')
        self.account_warning_lbl.setText('')
        self.savings_warning_lbl.setText('')

        self.stackedWidget.setCurrentIndex(2)

    def load_data(self, name: str, balance: float) -> None:
        """
        takes the data given from the csv file for an account and uploads it to account balance and name.
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
        if name == 'nil':
            self.account_warning_lbl.setText('Account cannot be nil')
            return
        self.account_name_lnedit.clear()
        self.__account_name = name

        try:
            with open('accounts.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for line in csv_reader:
                    if line[0] == name:
                        self.load_data(line[0], float(line[1]))
                        return  # Account found, no need to proceed further

            # If the account is not found, append it to the end of the file
                with open('accounts.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    new_data = [name, 0, 100, 0]
                    csv_writer.writerow(new_data)
                for line in csv_reader:
                    if line[0] == name:
                         self.load_data(line[0], float(line[1]))

        except FileNotFoundError:
            # If the file doesn't exist, create it and add the new account
            with open('accounts.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                new_data = [name, 0, 100, 0]
                csv_writer.writerow(new_data)

            with open('accounts.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    if line[0] == name:
                        self.load_data(line[0], float(line[1]))

        self.display_balance()

    def switch_page(self, index) -> None:
        """
        function changes which of the stacked widget pages gets displayed
        :param index: the index of the page to switch to
        :return: none
        """
        if self.__account_name == 'nil':
            self.account_warning_lbl.setText('Enter account before switching tabs')
            return
        else:
            self.stackedWidget.setCurrentIndex(index)
            self.display_balance()

    def display_balance(self) -> None:
        """
        function updates the balance to display
        :return: none
        """
        self.balance_label.setText(f'Balance: ${self.get_balance(1):.2f}')
        self.savings_balance_lbl.setText(f'Balance: ${self.get_balance(2):.2f}')
        self.savings_warning_lbl.setText('')
        self.warning_lbl.setText('')
        self.account_warning_lbl.setText('')

    def save_account(self) -> None:
        """
        uploads the current name and balance data to the csv file with matching account name
        :return: none
        """
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

    def get_balance(self, token: int) -> float:
        """
        accesses the csv_file and returns either the regular account balance or savings account balance
        :param token: 1 to access regular account 2 for savings account
        :return:
        """
        with open('accounts.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[0] == self.__account_name:
                    if token == 1:
                        value = line[1]
                    elif token == 2:
                        value = line[2]
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
            self.change_balance(self.get_balance(1) + amount)

        self.save_account()
        self.display_balance()

    def withdraw(self) -> None:
        """
        subtracts the value from user entry field from current balance
        :return: none
        """
        try:
            amount = float(self.user_entry.text())
        except ValueError:
            self.warning_lbl.setText(f'Can not accept value')
            return

        self.user_entry.clear()

        if amount > 0:
            self.change_balance(self.get_balance(1) - amount)

        self.save_account()
        self.display_balance()

    def apply_interest(self) -> None:
        """
        multiplies the savings balance by RATE every 5 transactions
        :return: none
        """
        with open('accounts.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            accounts = list(csv_reader)

        for line in accounts:
            if line and line[0] == self.__account_name:
                line[3] = str(int(line[3]) + 1)
                if line[3] == '5':
                    line[3] = '0'
                    line[2] = str(float(line[2]) * self.__RATE)

        with open('accounts.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(accounts)

    def deposit_savings(self) -> None:
        """
        adds the value from user entry filed to savings balance
        :return: none
        """
        try:
            amount = float(self.savings_lnedit.text())
        except ValueError:
            self.savings_warning_lbl.setText(f'Can not accept value')
            return

        self.savings_lnedit.clear()
        if amount > 0:
            self.change_savings(float(self.get_balance(2)) + amount)

        self.apply_interest()
        self.display_balance()

    def change_savings(self, value: float) -> None:
        """
        set the new savings balance and uploads to csv file
        :param value: the value to change the savings balance to
        :return: none
        """
        with open('accounts.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            accounts = list(csv_reader)

        for line in accounts:
            if line and line[0] == self.__account_name:
                line[2] = str(value)

        with open('accounts.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(accounts)
