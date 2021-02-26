import os
import json

from containers import DockerContainers

class DockerProjects:
    # Constructor
    def __init__(self):
        # self.rootDir = os.path.dirname(os.path.abspath(__file__))
        # self.projectsFile = os.path.join(self.rootDir, "projects.json")
        self.projectsFile = "projects.json"
        if os.path.exists(self.projectsFile) and os.path.isfile(self.projectsFile):
            self.projects = self.getProjects()
            self.mainLoop = True
            self.projectId = 0
            while self.mainLoop:
                self.showProjects()
                try:
                    command = input("Enter Command: ")
                    self.runCommand(command)
                except KeyboardInterrupt:
                    self.mainLoop = False
                    print("")
            os.system("clear")
        else:
            print("\033[1;31mYou need to create file \""+self.projectsFile+"\" with the projects.\033[0m")

    # Read Projects List
    def getProjects(self):
        f = open(self.projectsFile)
        projects = json.load(f)
        f.close()
        return projects

    def getProjectParam(self, paramName, projectId = -1):
        if projectId < 0:
            projectId = self.projectId
        return self.projects[projectId][paramName]

    # Print Title
    def printTitle(self, title):
        print("\033[48;5;4m            \033[1m\033[97m"+title+"\x1B[K\033[0m")

    # Show Documentations
    def showDocumentation(self):
        os.system("clear")
        self.printTitle("Extra Options")
        print("")
        print("s - Stop all containers\n\t1+s")
        print("d - Down all containers\n\t1+d")
        print("b - Build all containers\n\t1+b")
        print("")
        input("Press [Enter] key to continue...")

    # Show Projects
    def showProjects(self):
        os.system("clear")
        self.printTitle("Docker - Projects")
        i = 0
        print("")
        while i < len(self.projects):
            print("{0:3} - {1}".format(i+1, self.getProjectParam("name", i) ))
            i += 1
        print("")

    # Run Command
    def runCommand(self, cmd):
        cmds = cmd.split("+")
        if cmds[0] in ["x", "exit", "0"]:
            self.mainLoop = False
        elif cmds[0] in ["h", "help"]:
            self.showDocumentation()
        else:
            cmds[0] = int(cmds[0]) - 1
            if cmds[0] >= 0 and cmds[0] < len(self.projects):
                self.projectId = cmds[0]
            if len(cmds) > 1:
                if cmds[1] == "s":
                    self.stopProject()
                    input("\nPress [Enter] key to continue...")
                elif cmds[1] == "d":
                    self.downProject()
                    input("\nPress [Enter] key to continue...")
                elif cmds[1] == "b":
                    self.buildProject()
                    input("\nPress [Enter] key to continue...")
            else:
                # Start
                self.startProject()
                DContainers = DockerContainers(self.projects[self.projectId])
                self.stopProject()

    def startProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" up -d'
        os.system(cmd.format(self.getProjectParam("dockerPath")))

    def stopProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" stop'
        os.system(cmd.format(self.getProjectParam("dockerPath")))

    def downProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" down'
        os.system(cmd.format(self.getProjectParam("dockerPath")))

    def buildProject(self):
        os.system("clear")
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" build'
        os.system(cmd.format(self.getProjectParam("dockerPath")))
