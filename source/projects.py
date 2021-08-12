import os
import json
import readline # input history
import sys

from general    import General
from commands   import Commands
from containers import DockerContainers

class DockerProjects:
    # Constructor
    def __init__(self, version):
        self.version = version
        # Main loop
        self.mainLoop = True
        # Project ID
        self.projectId = 0

        try:
            self.projects = self.getProjects()
            while self.mainLoop:
                self.showProjects()
                inputCommands = input("Enter Command: ")
                classCommands = Commands(inputCommands)
                self.runCommands(classCommands)
        except KeyboardInterrupt:
            print("")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            General.errorMessage(exc_value)

    # Read projects list
    def getProjects(self):
        baseDir = self.getBaseDir()
        projectsFile = os.path.join(baseDir, "projects.json")
        if os.path.exists(projectsFile) and os.path.isfile(projectsFile):
            strem = open(projectsFile)
            projects = json.load(strem)
            strem.close()
            return projects
        else:
            raise Exception("The file with projects doesn't exist.")

    # Returns the base directory of the program
    def getBaseDir(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        if os.path.isfile(baseDir):
            baseDir = os.path.dirname(baseDir)
        return baseDir

    # Checking project by ID
    def checkProject(self, id):
        if id >= 0 and id < len(self.projects):
            if "dockerPath" in self.projects[id]:
                dockerComposeFile = os.path.join(self.projects[id]["dockerPath"], "docker-compose.yml")
                if os.path.exists(dockerComposeFile):
                    return True
        return False

    # Print title
    def printTitle(self, title, version = ""):
        print("\033[48;5;4m            \033[1m\033[97m{0}{1}\x1B[K\033[0m".format(title, version))

    # Show documentations
    def showDocumentation(self):
        General.clear()
        self.printTitle("Projects - Extra Options")
        print("")
        print("You can add additional parameters after the space.")
        print("")
        print("s - Stop all containers.")
        print("d - Down all containers.")
        print("b - Build all containers.")
        print("")
        General.pause()

    # Show projects
    def showProjects(self):
        General.clear()
        self.printTitle("Docker - Projects", " v"+self.version)
        i = 1
        print("")
        for project in self.projects:
            projectName = project["name"] if "name" in project else "???"
            if self.checkProject(i-1):
                print("{0:3} - {1}".format(i, projectName))
            else:
                print("{0:3} - \033[1;31m{1}\033[0m".format(i, projectName))
            i += 1
        print("")

    # Run commands
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

    # Run command
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
            # Set Project ID
            self.projectId = int(commandName) - 1
            if self.projectId < 0 or self.projectId >= len(self.projects):
                self.projectId = 0
                return False
            if self.checkProject(self.projectId) != True:
                projectName = self.projects[self.projectId]["name"] if "name" in self.projects[self.projectId] else "???"
                raise Exception("Project \"{0}\" don't have docker-compose.yml file.".format(projectName))
            # Apply command
            firstParam = command.getParam().getValue()
            if firstParam == "s":
                self.stopProject()
            elif firstParam == "d":
                self.downProject()
            elif firstParam == "b":
                self.buildProject()
            else:
                self.startProject()
                runDockerContainers = DockerContainers(self.projects[self.projectId])
                self.stopProject()
                return False
            return True
        return False

    # Start project
    def startProject(self):
        General.clear()
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" up -d'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))

    # Stop project
    def stopProject(self):
        General.clear()
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" stop'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))

    # Down project
    def downProject(self):
        General.clear()
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" down'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))

    # Build project
    def buildProject(self):
        General.clear()
        cmd = 'docker-compose --project-directory "{0}" --file "{0}/docker-compose.yml" build'
        os.system(cmd.format(self.projects[self.projectId]["dockerPath"]))
        self.isPause = True
