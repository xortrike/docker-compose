import os
import readline # input history
import sys

from general  import General
from commands import Commands

class ToolsTerminal:
    # Constructor
    def __init__(self, tools, containers, userName):
        self.config = tools
        self.containers = containers
        self.mainLoop = True
        self.openGroupByIndex = -1

        self.commands = self.getCommands()

        while self.mainLoop:
            self.showCommands()
            try:
                inputCommands = input("Enter Command: ")
                classCommands = Commands(inputCommands)
                self.runCommands(classCommands)
            except KeyboardInterrupt:
                self.mainLoop = False

    # Title
    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Return commands toolds.
    def getCommands(self):
        return [
            {
                "group": "MySQL",
                "commands": [
                    {"name": "Import Database", "method": "MySQLImport"},
                    {"name": "Export Database", "method": "MySQLExport"},
                    {"name": "Show Databases", "method": "MySQLShow"}
                ]
            },
            {
                "group": "XDebugger",
                "commands": [
                    {"name": "Enable", "method": "XDebuggerEnable"},
                    {"name": "Disable", "method": "XDebuggerDisable"},
                    {"name": "Status", "method": "XDebuggerStatus"}
                ]
            }
        ]

    # Show Commands
    def showCommands(self):
        General.clear()
        self.printTitle("Tools - Terminal")
        print("")
        g = 0
        while g < len(self.commands):
            if self.openGroupByIndex == g:
                print("{0:3} - \033[33m{1}\033[0m".format(g+1, self.commands[g]["group"]))
                i = 0
                countItems = len(self.commands[g]["commands"])
                n = str( len( str(countItems) ) )
                while i < countItems:
                    print( ("{0:3}.{1:"+n+"} - \033[32m{2}\033[0m").format(g+1, i+1, self.commands[g]["commands"][i]["name"]) )
                    i = i + 1
            else:
                print("{0:3} - {1}".format(g+1, self.commands[g]["group"]))
            g = g + 1
        print("")

    # Show Documentations
    def showDocumentation(self):
        General.clear()
        self.printTitle("Extra Options")
        print("")
        print("MySQL - 1 dbname")
        print("")
        input("Press [Enter] key to continue...")

    # Run container commands
    def runCommands(self, commands):
        General.clear()
        result = True
        try:
            for command in commands:
                result = self.runCommand(command)
                if result == False:
                    break
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            General.warningMessage(exc_value)
        if result == True:
            General.pause()

    # Run Command
    def runCommand(self, command):
        self.openGroupByIndex = -1
        commandName = command.getCommand()
        # General commands
        if commandName in ["x", "exit", "0"]:
            self.mainLoop = False
            return False
        elif commandName in ["h", "help"]:
            self.showDocumentation()
            return False
        elif commandName.isnumeric():
            commandName = int(commandName) - 1
            if command.getSubCommand() and commandName < len(self.commands):
                subCommandName = int(command.getSubCommand()) - 1
                if subCommandName < len(self.commands[commandName]["commands"]):
                    params = command.getParams()
                    return getattr(self, self.commands[commandName]["commands"][subCommandName]["method"])(params)
            else:
                self.openGroupByIndex = commandName
        return False

    def MySQL(self):
        # MySQL Container
        if "mysqlContainer" not in self.config:
            raise Exception("In your configuration don't have a MySQL container name.")
        if self.config["mysqlContainer"] not in self.containers:
            raise Exception("Container \"{0}\" not found.".format(self.config["mysqlContainer"]))
        # MySQL User
        if "mysqlUser" not in self.config:
            raise Exception("In your configuration don't have a MySQL user name.")
        # MySQL Password
        if "mysqlPassword" not in self.config:
            raise Exception("In your configuration don't have a MySQL user password.")

    def MySQLExport(self, params):
        General.clear()
        self.MySQL()

        dbName = params.getParam().getValue()
        if not len(dbName):
            raise Exception("Set database name.")
        container = self.config["mysqlContainer"]
        user = self.config["mysqlUser"]
        password = self.config["mysqlPassword"]

        exportPath = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(exportPath):
            exportPath = os.path.dirname(exportPath)
        if "mysqlDumpDir" in self.config and os.path.exists(self.config["mysqlDumpDir"]):
            exportPath = self.config["mysqlDumpDir"]
        exportPath = os.path.join(exportPath, "{0}.sql".format(dbName))

        os.system("clear")
        print("Export database \"{0}\" to: {1}".format(dbName, exportPath))
        os.system("docker exec {0} mysqldump --user={1} --password={2} {3} > \"{4}\"".format(container, user, password, dbName, exportPath))
        return True

    def MySQLImport(self, params):
        General.clear()
        self.MySQL()

        dbName = params.getParam().getValue()
        if not len(dbName):
            raise Exception("Set database name.")
        container = self.config["mysqlContainer"]
        user = self.config["mysqlUser"]
        password = self.config["mysqlPassword"]

        importPath = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(importPath):
            importPath = os.path.dirname(importPath)
        if "mysqlDumpDir" in self.config and os.path.exists(self.config["mysqlDumpDir"]):
            importPath = self.config["mysqlDumpDir"]
        importPath = os.path.join(importPath, "{0}.sql".format(dbName))

        General.clear()
        print("Import database \"{0}\" from: {1}".format(dbName, importPath))
        os.system("cat \"{4}\" | docker exec -i {0} mysql --user={1} --password={2} --database={3}".format(container, user, password, dbName, importPath))
        return True

    def MySQLShow(self, params):
        General.clear()
        self.MySQL()
        container = self.config["mysqlContainer"]
        user = self.config["mysqlUser"]
        password = self.config["mysqlPassword"]

        print("Available databases:\n")
        stream = os.popen("docker exec -i {0} mysql --user={1} --password={2} --execute=\"{3}\"".format(container, user, password, "SHOW DATABASES;"))
        output = stream.read()
        lines = output.split("\n")
        i = 1
        while i < len(lines) - 1:
            print(" - {0}".format(lines[i]))
            i = i + 1
        return True

    def XDebugger(self):
        # PHP Container
        if "phpContainer" not in self.config:
            raise Exception("In your configuration don't have a PHP container name.")
        if self.config["phpContainer"] not in self.containers:
            raise Exception("Container \"{0}\" not found.".format(self.config["phpContainer"]))

    def XDebuggerExist(self):
        container = self.config["phpContainer"]
        checkFile = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"

        stream = os.popen("docker exec {0} bash -c \"if [ -f {1} ] || [ -f {1}.bak ]; then echo 1; else echo 0; fi\"".format(container, checkFile))
        output = stream.read()

        return True if int(output) else False

    def XDebuggerEnable(self, params):
        General.clear()
        self.XDebugger()

        container = self.config["phpContainer"]
        moveFrom = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini.bak"
        moveTo = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"

        print("XDebugger - Enable\n")

        if not self.XDebuggerExist():
            raise Exception("XDebugger module not found.")

        os.system("docker exec {0} bash -c \"if [ -f {1} ]; then mv {1} {2}; fi\"".format(container, moveFrom, moveTo))
        os.system("docker restart {0}".format(container))
        print("XDebugger was enabled.")
        return True

    def XDebuggerDisable(self, params):
        General.clear()
        self.XDebugger()

        container = self.config["phpContainer"]
        moveFrom = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"
        moveTo = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini.bak"

        print("XDebugger - Disable\n")

        if not self.XDebuggerExist():
            raise Exception("XDebugger module not found.")

        os.system("docker exec {0} bash -c \"if [ -f {1} ]; then mv {1} {2}; fi\"".format(container, moveFrom, moveTo))
        os.system("docker restart {0}".format(container))
        print("XDebugger was disabled.")
        return True

    def XDebuggerStatus(self, params):
        General.clear()
        self.XDebugger()

        container = self.config["phpContainer"]
        checkFile = "/usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini"

        print("XDebugger - Status\n")

        if not self.XDebuggerExist():
            raise Exception("XDebugger module not found.")

        stream = os.popen("docker exec {0} bash -c \"if [ -f {1} ]; then echo 1; else echo 0; fi\"".format(container, checkFile))
        output = stream.read()

        print("XDebugger is enabled." if int(output) else "XDebugger is disabled.")

        return True
