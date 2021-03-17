import os

from magento    import MagentoTerminal
from mysql      import MySqlTerminal

class DockerContainers:
    # Constructor
    def __init__(self, project):
        self.isPause = False
        self.mainLoop = True
        self.project = project
        self.containers = []
        while self.mainLoop:
            self.isPause = False
            self.showContainers()
            try:
                command = input("Enter Command: ")
                self.runCommand(command)
            except KeyboardInterrupt:
                self.mainLoop = False
                print("")
            except Exception as errorMessage:
                os.system("clear")
                print(errorMessage)
                self.isPause = True
            if self.isPause:
                input("\nPress [Enter] key to continue...")

    def getContainers(self):
        stream = os.popen('docker container ls --format "{{.Names}}"')
        output = stream.read()
        self.containers = list(filter(None, output.split("\n")))
        return self.containers

    # Documentations
    def showDocumentation(self):
        os.system("clear")
        self.printTitle("Extra Options")
        print("")
        print("u - Open container as another user\n\t1+u=www-data")
        print("mage - Run Magento terminal")
        print("sql - Run SQL terminal")
        print("")
        input("Press [Enter] key to continue...")

    # Print Title
    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show Containers
    def showContainers(self):
        os.system("clear")
        self.printTitle("Docker - Containers")
        print("")
        i = 0
        containers = self.getContainers()
        while i < len(containers):
            print("{0:3} - {1}".format(i+1, containers[i]))
            i += 1
        print("")

    def runCommand(self, cmd):
        cmds = cmd.split("+")
        if cmds[0] in ["x", "exit", "0"]:
            self.mainLoop = False
        elif cmds[0] in ["h", "help"]:
            self.showDocumentation()
        elif cmds[0] == "mage":
            if "mage" in self.project:
                magento = MagentoTerminal(self.project["mage"], self.containers)
            else:
                os.system("clear")
                print("\033[1;31mIn your configuration file don't have \"mage\" configuration.\033[0m")
                self.isPause = True
        elif cmds[0] == "sql":
            if "sql" in self.project:
                mysql = MySqlTerminal(self.project["sql"], self.containers)
            else:
                os.system("clear")
                print("\033[1;31mIn your configuration file don't have \"sql\" configuration.\033[0m")
                self.isPause = True
        elif cmds[0].isnumeric():
            # Base
            cmds[0] = int(cmds[0]) - 1
            if cmds[0] >= 0 and cmds[0] < len(self.containers):
                if len(cmds) > 1:
                    params = cmds[1].split("=")
                    if params[0] == "u":
                        # Open container as user...
                        userName = params[1]
                        containerName = self.containers[cmds[0]]
                        os.system('docker exec -it --user {0} {1} /bin/bash'.format(userName, containerName))
                else:
                    # Open container
                    os.system("clear")
                    containerName = self.containers[cmds[0]]
                    os.system('docker exec -it {0} /bin/bash'.format(containerName))
