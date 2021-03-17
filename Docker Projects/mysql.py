import os

class MySqlTerminal:
    # Constructor
    def __init__(self, mysql, containers):
        self.config = mysql
        self.mainLoop = True
        self.isPause = False

        if "container" not in self.config:
            raise Exception("In your configuration don't have a MySQL container name.")
        if self.config["container"] not in containers:
            raise Exception("Container \"{0}\" not found.".format(self.config["container"]))
        if "user" not in self.config:
            raise Exception("In your configuration don't have mysql user name.")
        if "password" not in self.config:
            raise Exception("In your configuration don't have mysql user password.")

        while self.mainLoop:
            self.isPause = False
            self.showCommands()
            try:
                command = input("Enter Command: ")
                self.runCommand(command)
                if self.isPause:
                    input("\nPress [Enter] key to continue...")
            except KeyboardInterrupt:
                self.mainLoop = False

    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show Commands
    def showCommands(self):
        os.system("clear")
        self.printTitle("MySQL - Terminal")
        print("")
        print("1. Export Database")
        print("2. Import Database")
        print("3. Show Databases")
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
        elif cmds[0].isnumeric():
            if cmds[0] == "1":
                # Import
                if len(cmds) > 1:
                    self.exportDatabase(cmds[1])
                else:
                    print("Please enter database name.")
                    self.isPause = True
            elif cmds[0] == "2":
                # Export
                if len(cmds) > 1:
                    self.importDatabase(cmds[1])
                else:
                    print("Please enter database name.")
                    self.isPause = True
            elif cmds[0] == "3":
                # Show
                self.showDatabases()

    # Export Database
    def exportDatabase(self, db):
        container = self.config["container"]
        user = self.config["user"]
        password = self.config["password"]

        exportPath = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(exportPath):
            exportPath = os.path.dirname(exportPath)
        if "dumpDir" in self.config and os.path.exists(self.config["dumpDir"]):
            exportPath = self.config["dumpDir"]
        exportPath = os.path.join(exportPath, "{0}.sql".format(db))

        os.system("clear")
        print("Export database: {0}\nExport to path: {1}".format(db, exportPath))
        os.system("docker exec {0} mysqldump --user={1} --password={2} {3} > \"{4}\"".format(container, user, password, db, exportPath))
        self.isPause = True

    # Import Database
    def importDatabase(self, db):
        container = self.config["container"]
        user = self.config["user"]
        password = self.config["password"]

        importPath = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(importPath):
            importPath = os.path.dirname(importPath)
        if "dumpDir" in self.config and os.path.exists(self.config["dumpDir"]):
            importPath = self.config["dumpDir"]
        importPath = os.path.join(importPath, "{0}.sql".format(db))

        os.system("clear")
        print("Import database: {0}\nImport from path: {1}".format(db, importPath))
        os.system("cat \"{4}\" | docker exec -i {0} mysql --user={1} --password={2} --database={3}".format(container, user, password, db, importPath))
        self.isPause = True

    def showDatabases(self):
        os.system("clear")
        container = self.config["container"]
        user = self.config["user"]
        password = self.config["password"]
        print("Available databases:\n")
        stream = os.popen("docker exec -i {0} mysql --user={1} --password={2} --execute=\"{3}\"".format(container, user, password, "SHOW DATABASES;"))
        output = stream.read()
        lines = output.split("\n")
        i = 1
        while i < len(lines) - 1:
            print(" - {0}".format(lines[i]))
            i = i + 1
        self.isPause = True
