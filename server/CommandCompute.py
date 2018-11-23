def getCommand(commandStr):
    s = ""
    i = 0

    com = []
    while i < len(commandStr):
        if (commandStr[i] == '/'):
            com.append(s)
            s = ""
        else:
            s += commandStr[i]
        i+=1
    com.append(s)
    return com
def getCommandGsm(commandStr):
    s = ""
    i = 0

    com = []
    while i < len(commandStr):
        if (commandStr[i] == '|'):
            com.append(s)
            s = ""
        else:
            s += commandStr[i]
        i+=1
    com.append(s)
    if(len(com) > 1):
        return getCommand(com[1])
    else:
        return []

def getStr(commandList):
    s = ""
    if len(commandList) > 0:
        s += commandList[0]
    for command in range(1,len(commandList)):
        s += '/' + commandList[command]
    return s
