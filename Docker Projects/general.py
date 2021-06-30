import os

class General:
    # Emulation pause
    @staticmethod
    def pause():
        input("\nPress [Enter] key to continue...")

    # Clear output
    @staticmethod
    def clear():
        os.system("clear")

    # Show error message
    @staticmethod
    def errorMessage(message):
        print("\033[1;31mError: {0}\033[0m".format(message))

    # Show warning message
    @staticmethod
    def warningMessage(message):
        print("\033[38;5;208mWarning: {0}\033[0m".format(message))
