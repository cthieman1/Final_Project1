from PyQt6.QtWidgets import *
from gui import *

class Accounts(QMainWindow, Ui_MainWindow):

    def __init__(self, name, balance=0):
        super().__init__()
        self.setupUi(self)
        self.__account_name = name
        self.__account_balance = balance

        self.set_balance_button.clicked.connect(lambda : self.set_balance())

        self.set_balance(0)

    def display_balance(self):
        self.balance_label.setText(f'Balance: {self.__account_balance}')

    def set_balance(self, value=0):
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






