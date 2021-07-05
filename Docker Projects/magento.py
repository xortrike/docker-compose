import os
import readline # input history
import sys
import re

from general import General
from commands import Commands

class MagentoTerminal:
    # Constructor
    def __init__(self, config, containers, userName):
        self.config = config
        self.title = "Magento 2 - Terminal"
        self.commands = []
        self.mainLoop = True
        self.openGroupByIndex = -1

        # Exist container name
        if "container" not in self.config:
            raise Exception("In your configuration don't have a PHP container name.")
        # Exist container by name
        if self.config["container"] not in containers:
            raise Exception("Container \"{0}\" not running.".format(self.config["container"]))
        # Set new user name
        if len(userName):
            self.config["user"] = userName

        self.commands = self.readCommandsList()
        if not self.commands or len(self.commands) == 0:
            raise Exception("Something went wrong.")

        while self.mainLoop:
            self.showCommands()
            try:
                inputCommands = input("Enter Command: ")
                classCommands = Commands(inputCommands)
                self.runCommands(classCommands)
            except KeyboardInterrupt:
                self.mainLoop = False

    def readCommandsList(self):
        General.clear()
        print("\033[32mReading commands list...\033[0m")
        # Read data
        stream = os.popen('docker exec --user {0} {1} php bin/magento list'.format(self.config["user"], self.config["container"]))
        output = stream.read()
        lines = output.split("\n")
        # lines = output.splitlines(True)
        # Parse data
        i = 0
        commands = []
        # Skip information
        while i < len(lines):
            if lines[i] == "Available commands:":
                i += 3
                break
            else:
                i += 1
        # Read commands
        while i < len(lines):
            if lines[i][:2] == "  ":
                spaces = re.findall(r'\s{2,}', lines[i][2:])
                comDeslist = re.split(r'{0}'.format(spaces[0]), lines[i][2:])
                commands[-1]["commands"].append({
                    "command": comDeslist[0],
                    "description": comDeslist[1]
                })
            elif lines[i][:1] == " ":
                commands.append({
                    "group": lines[i][1:],
                    "commands": []
                })
            i += 1
        return commands

    # Print title
    def printTitle(self, title):
        user = self.config["user"] if "user" in self.config else "root"
        print("\033[48;5;202m            \033[1m\033[97m"+title+" ["+user+"]\x1B[K\033[0m")

    # Show Commands
    def showCommands(self, n = 0):
        os.system("clear")
        self.printTitle(self.title)
        print("")
        g = 0
        while g < len(self.commands):
            if "groups" in self.config and len(self.config["groups"]) > 0 and self.commands[g]["group"] not in self.config["groups"]:
                g = g + 1
                continue
            if self.openGroupByIndex == g:
                print("{0:3} - \033[33m{1}\033[0m".format(g+1, self.commands[g]["group"]))
                i = 0
                countCommands = len(self.commands[g]["commands"])
                # Count Subcommands (string length)
                n = str( len( str(countCommands) ) )
                # Max string length subcommands
                maxLength = str(max(len(node["command"]) for node in self.commands[g]["commands"]) + 8)
                # Show subcommands
                while i < countCommands:
                    print(("{0:3}.{1:"+n+"} - \033[32m{2:"+maxLength+"}\033[0m{3}\033[0m").format(
                            g+1,
                            i+1,
                            self.commands[g]["commands"][i]["command"],
                            self.commands[g]["commands"][i]["description"]
                        )
                    )
                    i = i + 1
            else:
                print("{0:3} - {1}".format(g+1, self.commands[g]["group"]))
            g = g + 1
        print("")

    # Show Documentations
    def showDocumentation(self):
        os.system("clear")
        self.printTitle("Extra Options")
        print("")
        print("; - Multiple-Commands\n    Example: 1.1;1.2;1.3")
        print("+ - Add param to command\n    Example: 1.1+Vendor_Module")
        print("")

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

    def runCommand(self, command):
        commandName = command.getCommand()
        # General commands
        if commandName in ["x", "exit", "0"]:
            self.mainLoop = False
            return False
        elif commandName in ["h", "help"]:
            self.showDocumentation()
            return False
        elif commandName.isnumeric():
            commandIdx = int(commandName) - 1
            if command.getSubCommand() and commandIdx < len(self.commands):
                subCommandIdx = int(command.getSubCommand()) - 1
                if subCommandIdx < len(self.commands[commandIdx]["commands"]):
                    magentoCommand = self.commands[commandIdx]["commands"][subCommandIdx]["command"]
                    stringParams = command.getParamsAsString()
                    print("\033[33m[{0}] [{1}]\033[0m".format(magentoCommand, stringParams))
                    os.system('docker exec -it --user {1} {0} php bin/magento {2} {3}'.format(
                        self.config["container"],
                        self.config["user"],
                        magentoCommand,
                        stringParams
                    ))
                    return True
            else:
                self.openGroupByIndex = commandIdx

        return False
