import os
import json

from containers import DockerContainers

class DockerProjects:
    # Constructor
    def __init__(self):
        self.isPause = False
        self.rootDir = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(self.rootDir):
            self.rootDir = os.path.dirname(self.rootDir)
        self.projectsFile = os.path.join(self.rootDir, "projects.json")
        if os.path.exists(self.projectsFile) and os.path.isfile(self.projectsFile):
            self.projects = self.getProjects()
            self.mainLoop = True
            self.projectId = 0
            while self.mainLoop:
                self.isPause = False
                self.showProjects()
                try:
                    command = input("Enter Command: ")
                    self.runCommand(command)
                    if self.isPause:
                        input("\nPress [Enter] key to continue...")
                except KeyboardInterrupt:
                    self.mainLoop = False
                    print("")
            os.system("clear")
        else:
            os.system("clear")
            print("\033[1;31mYou need to create file \""+self.projectsFile+"\" with the projects.\033[0m")
            input("\nPress [Enter] key to continue...")

    # Read Projects List
    def getProjects(self):
        f = open(self.projectsFile)
        projects = json.load(f)
        f.close()
        return projects

    # Print Title
    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show Documentations
    def showDocumentation(self):
        os.system("clear")
        self.printTitle("Extra Options")
        print("We can add extra options via plus.")
        print("")
        print("s - Stop all containers\n    Example: 1+s")
        print("d - Down all containers\n    Example: 1+d")
        print("b - Build all containers\n    Example: 1+b")
        print("")
        self.isPause = True

    # Show Projects
    def showProjects(self):
        os.system("clear")
        self.printTitle("Docker - Projects")
        i = 0
        print("")
        while i < len(self.projects):
            if "name" in self.projects[i] and "dockerPath" in self.projects[i]:
                pathDockerCompose = os.path.join(self.projects[i]["dockerPath"], "docker-compose.yml")
                if os.path.exists(pathDockerCompose):
                    print("{0:3} - {1}".format(i+1, self.projects[i]["name"]))
                else:
                    print("{0:3} - \033[1;31m{1}\033[0m".format(i+1, self.projects[i]["name"]))
            i += 1
        print("")

    # Run Command
    def runCommand(self, cmd):
        cmds = cmd.split("+")
        if cmds[0] in ["x", "exit", "0"]:
            self.mainLoop = False
        elif cmds[0] in ["h", "help"]:
            self.showDocumentation()
        elif cmds[0].isnumeric():
            cmds[0] = int(cmds[0]) - 1
            if cmds[0] >= 0 and cmds[0] < len(self.projects):
                self.projectId = cmds[0]
                if len(cmds) > 1:
                    # Params
                    if cmds[1] == "s":
                        self.stopProject()
                    elif cmds[1] == "d":
                        self.downProject()
                    elif cmds[1] == "b":
                        self.buildProject()
                else:
                    pathDockerCompose = os.path.join(self.projects[self.projectId]["dockerPath"], "docker-compose.yml")
                    if os.path.exists(pathDockerCompose):
                        # Start
                        self.startProject()
                        DContainers = DockerContainers(self.projects[self.projectId])
                        self.stopProject()
                    else:
                        os.system("clear")
                        print("\033[1;31mProject \"{0}\" don't have docker-compose.yml file.\033[0m".format(self.projects[self.projectId]["name"]))
                        self.isPause = True

    def startProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" up -d'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))

    def stopProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" stop'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))

    def downProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" down'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))

    def buildProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" build'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))
