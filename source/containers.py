import os
import readline # input history
import sys

from general  import General
from commands import Commands
from magento  import MagentoTerminal
from tools    import ToolsTerminal

class DockerContainers:
    # Constructor
    def __init__(self, project):
        # Project details
        self.project = project
        # Main loop
        self.mainLoop = True

        try:
            while self.mainLoop:
                self.containers = self.getContainers()
                self.showContainers()
                inputCommands = input("Enter Command: ")
                classCommands = Commands(inputCommands)
                self.runCommands(classCommands)
        except KeyboardInterrupt:
            print("")
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            General.errorMessage(exc_value)

    # Return project name
    def getProjectName(self):
        return self.project["name"] if "name" in self.project else "???"

    # Return containers list
    def getContainers(self):
        stream = os.popen('docker container ls --format "{{.Names}}"')
        output = stream.read()
        containers = filter(None, output.split("\n"))
        return list(containers)

    # Show documentations
    def showDocumentation(self):
        General.clear()
        self.printTitle("Containers - Extra Options")
        print("")
        print("You can add additional parameters after the space.")
        print("")
        print("        u - Open container as another user [1 -u=www-data]")
        print("m/magento - Open Magento 2 terminal.")
        print("  t/tools - Open special tools terminal.")
        print("")
        General.pause()

    # Print title
    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show containers list
    def showContainers(self):
        General.clear()
        self.printTitle("{0} - Containers".format(self.getProjectName()))
        i = 1
        print("")
        for container in self.containers:
            print("{0:3} - {1}".format(i, container))
            i += 1
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

    # Run container command
    def runCommand(self, command):
        commandName = command.getCommand()
        # Default user
        userName = command.getParam("u").getValue()

        # General commands
        if commandName in ["x", "exit", "0"]:
            self.mainLoop = False
            return False
        elif commandName in ["h", "help"]:
            self.showDocumentation()
            return False
        elif commandName in ["m", "magento"]:
            # MAGE
            if not "magento" in self.project:
                raise Exception("In your configuration file don't have \"magento\" configuration.")
            config = self.project["magento"].copy()
            if len(userName):
                config["user"] = userName
            MagentoTerminal(config, self.containers.copy())
            readline.clear_history()
            return False
        elif commandName in ["t", "tools"]:
            # TOOLS
            if not "tools" in self.project:
                raise Exception("In your configuration file don't have \"tools\" configuration.")
            config = self.project["tools"].copy()
            if len(userName):
                config["user"] = userName
            ToolsTerminal(config, self.containers.copy())
            readline.clear_history()
            return False
        elif commandName.isnumeric():
            userName = userName if len(userName) else "root"
            containerName = self.containers[int(commandName)-1]
            os.system('docker exec -it --user {0} {1} /bin/bash'.format(userName, containerName))

        return False
