import os

class MagentoTerminal:
    # Constructor
    def __init__(self, phpContainerName):
        self.phpContainerName = phpContainerName
        self.title = "Magento 2 - Terminal"
        self.commands = []
        self.mainLoop = True
        self.openGroupByIndex = -1
        self.isPause = False
        self.readCommandsList()
        while self.mainLoop:
            self.showCommands()
            try:
                command = input("Enter Command: ")
                os.system("clear")
                for com in command.split(";"):
                    self.runCommand(com)
                if self.isPause:
                    input("Press [Enter] key to continue...")
            except KeyboardInterrupt:
                self.mainLoop = False
                print("")

    def readCommandsList(self):
        os.system("clear")
        print("\033[32mReading commands list...\033[0m")
        stream = os.popen('docker exec {0} php bin/magento list'.format(self.phpContainerName))
        output = stream.read()
        lines = output.split("\n")
        if len(lines[0]):
            self.title = lines[0]
        i = 17 if lines[14] == "Available commands:" else 0

        while i < len(lines):
            if len(lines[i]) > 0:
                if lines[i][:2] == "  ":
                    self.commands[-1]["commands"].append(lines[i][2:])
                    # self.commands[-1]["commands"].append({
                    #     "command": lines[i][2:][:44].strip(),
                    #     "description": lines[i][2:][44:]
                    # })
                elif lines[i][:1] == " ":
                    self.commands.append({
                        "group": lines[i][1:],
                        "commands": []
                    })
            i = i + 1

    def printTitle(self, title):
        print("\033[48;5;202m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show Commands
    def showCommands(self, n = 0):
        os.system("clear")
        self.printTitle(self.title)
        print("")
        g = 0
        while g < len(self.commands):
            if self.openGroupByIndex == g:
                print("{0:3} - \033[33m{1}\033[0m".format(g+1, self.commands[g]["group"]))
                i = 0
                countItems = len(self.commands[g]["commands"])
                n = str( len( str(countItems) ) )
                while i < countItems:
                    print( ("{0:3}.{1:"+n+"} - \033[32m{2}\033[0m{3}\033[0m").format(g+1, i+1, self.commands[g]["commands"][i][:44], self.commands[g]["commands"][i][44:] ) )
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
        print("; - Multiple-Commands\n\t1.1;1.2;1.3")
        print("+ - Add param to command\n\t1.1+Vendor_Module [module:enable Vendor_Module]")
        print("")

    def runCommand(self, cmd):
        cmds = cmd.split("+")
        if cmds[0] in ["x", "exit", "0"]:
            self.mainLoop = False
        elif cmds[0] == "h" or cmds[0] == "help":
            self.showDocumentation()
            self.isPause = True
        else:
            num = cmds[0].split(".")
            if len(num) == 1:
                self.openGroupByIndex = int(num[0]) - 1
            elif len(num) == 2:
                self.openGroupByIndex = -1
                self.isPause = True
                command = self.commands[int(num[0])-1]["commands"][int(num[1])-1][:44].strip()
                if len(cmds) > 1:
                    print("\033[33m["+command+"] ["+cmds[1]+"]\033[0m")
                    os.system('docker exec {0} php bin/magento {1} {2}'.format(self.phpContainerName, command, cmds[1]))
                else:
                    print("\033[33m["+command+"]\033[0m")
                    os.system('docker exec {0} php bin/magento {1}'.format(self.phpContainerName, command))
                print("")
