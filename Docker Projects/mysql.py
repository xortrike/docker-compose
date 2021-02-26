import os

class MySqlTerminal:
    # Constructor
    def __init__(self, sqlContainerName, user = "", password = ""):
        self.sqlContainerName = sqlContainerName
        self.sqlUser = user
        self.sqlPassword = password
        self.mainLoop = True
        while self.mainLoop:
                self.showCommands()
                try:
                    command = input("Enter Command: ")
                    self.runCommand(command)
                except KeyboardInterrupt:
                    self.mainLoop = False
                    print("")
        # input("Press [Enter] key to continue...")

    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show Commands
    def showCommands(self):
        os.system("clear")
        self.printTitle("MySQL - Terminal")
        print("")
        print("1. Export Database")
        print("2. Import Database")
        print("")

    # Show Documentations
    def showDocumentation(self):
        os.system("clear")
        self.printTitle("Extra Options")
        print("")
        print("+ - Add params\n\t1+userName password dbName\n\tIt you set user name and password to project propertyes, you can set only db name.")
        print("")
        input("Press [Enter] key to continue...")

    # Run Command
    def runCommand(self, cmd):
        cmds = cmd.split("+")
        if cmds[0] in ["x", "exit", "0"]:
            self.mainLoop = False
        elif cmds[0] in ["h", "help"]:
            self.showDocumentation()
        elif len(cmds) > 1:
            options = cmds[1].split(" ")
            if len(options) == 1:
                options = [
                    self.sqlUser,
                    self.sqlPassword,
                    cmds[1]
                ]
            if cmds[0] == "1":
                self.exportDatabase(options[0], options[1], options[2])
            elif cmds[0] == "2":
                self.importDatabase(options[0], options[1], options[2])

    # Export Database
    def exportDatabase(self, user, password, db):
        os.system("clear")
        print("Exporting database...")
        print("User: [\033[32m{0}\033[0m] Password: [\033[32m{1}\033[0m] Database: [\033[32m{2}\033[0m]".format(user, password, db))
        os.system("docker exec {0} mysqldump --user={1} --password={2} {3} > {3}.sql".format(self.sqlContainerName, user, password, db))
        input("Press [Enter] key to continue...")

    # Import Database
    def importDatabase(self, user, password, db):
        os.system("clear")
        print("Importing database...")
        print("User: [\033[32m{0}\033[0m] Password: [\033[32m{1}\033[0m] Database: [\033[32m{2}\033[0m]".format(user, password, db))
        os.system("cat {3}.sql | docker exec -i {0} mysql --user={1} --password={2} {3}".format(self.sqlContainerName, user, password, db))
        input("Press [Enter] key to continue...")
