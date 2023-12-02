from accounts import *

def main():
    application = QApplication([])
    window = Accounts()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()