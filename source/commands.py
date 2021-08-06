# SearchMe = "The apple is red and the berry is blue!"
# print(SearchMe.find("is"))
# print(SearchMe.rfind("is"))
# print(SearchMe.count("is"))
# print(SearchMe.startswith("The"))
# print(SearchMe.endswith("The"))
# print(SearchMe.replace("apple", "car")
#   .replace("berry", "truck"))

# "" - str
# [] - list
# {} - dict

class Commands:
    # Constructor
    def __init__(self, inputString):
        self.i = 0
        self.commands = []
        if len(inputString) > 0:
            for commandString in inputString.split(";"):
                self.commands.append(Command(commandString))

    # Iterable object
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.commands):
            self.i = self.i + 1
            return self.commands[self.i-1]
        else:
            raise StopIteration

    # Return commands list
    def getCommands(self):
        return self.commands

    # Return first command or by index
    def getCommand(self, idx = 1):
        if type(idx) == int or (type(idx) == str and idx.isnumeric()):
            idx = int(idx)
        if type(idx) == int and (idx > 0 and idx <= len(self.commands)):
            return self.commands[idx-1]
        return None

    # Return params list
    def getParams(self, idx = 1):
        command = self.getCommand(idx)
        return command.getParams() if command else None

    # Return first param or by key
    def getParam(self, idx = 1, key = 1):
        params = self.getParams(idx)
        return params.getParam(key) if params else None

class Command:
    # Constructor
    def __init__(self, commandString):
        self.command = None
        self.subcommand = None
        self.params = None

        if len(commandString) > 0:
            commands = commandString.strip().split(" ")
            point = commands[0].find(".")
            if point > 0:
                self.command = commands[0][0:point].strip()
                self.subcommand = commands[0][point+1:].strip()
            else:
                self.command = commands[0]
            self.params = Params(commands[1:])

    def __str__(self):
        return self.getCommand()

    # Return command
    def getCommand(self):
        return self.command

    # Return sub command
    def getSubCommand(self):
        return self.subcommand

    def getParams(self):
        return self.params

    # Return first param or by key
    def getParam(self, key = 1):
        return self.getParams().getParam(key)

    def getParamsAsString(self):
        strParams = []
        for param in self.getParams():
            strParams.append(param.getOriginal())
        return " ".join(strParams)

# Return Params object
class Params:
    # Constructor
    def __init__(self, paramsList):
        self.i = 0
        self.params = []
        for paramString in paramsList:
            if len(paramString) > 0:
                self.params.append(Param(paramString))

    # def __str__(self):
    #     return " ".join(map(str, params))

    # Iterable object
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.params):
            self.i = self.i + 1
            return self.params[self.i-1]
        else:
            raise StopIteration

    def getParam(self, key = 1):
        if type(key) == int or (type(key) == str and key.isnumeric()):
            id = int(key) - 1
            if id >= 0 and id < len(self.params):
                return self.params[id]
        else:
            for param in self.params:
                if param.getKey() == key:
                    return param
        return Param()

# Return Param object
class Param:
    # Constructor
    def __init__(self, paramString = ""):
        self.key = None
        self.value = None
        self.original = paramString
        if paramString.startswith("-") and paramString.count("=") == 1:
            keyValue = paramString.split("=")
            self.key = keyValue[0][1:].strip()
            self.value = keyValue[1].strip()
        else:
            self.value = paramString

    def __str__(self):
        return self.getValue()

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def getOriginal(self):
        return self.original
