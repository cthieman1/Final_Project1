from PyQt6.QtWidgets import *
from gui import *

class Accounts(QMainWindow, Ui_MainWindow):

    def __init__(self, name, balance=0):
        super().__init__()
        self.setupUi(self)
        self.__account_name = name
        self.__account_balance = balance

        self.set_balance_button.clicked.connect(lambda : self.set_balance())
        self.deposit_button.clicked.connect(self.deposit)


        self.set_balance()

    def display_balance(self):
        self.balance_label.setText(f'Balance: {self.get_balance()}')

    def change_balance(self, value=0):
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


    def set_balance(self):
        try:
            value = float(self.user_entry.text())
        except ValueError:
            value = 0

        self.user_entry.clear()

        if value > 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0

        self.display_balance()

    def get_balance(self):
        return self.__account_balance


    def deposit(self):
        try:
            amount = float(self.user_entry.text())
        except ValueError:
            #TODO create prompts for blank or incorrect submissions
            amount = 0

        self.user_entry.clear()
        if amount > 0:
            self.change_balance(self.get_balance() + amount)

        self.display_balance()

