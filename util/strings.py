def stripPrefix(string, split):
    return split.join(string.split(split)[1:])

def addPrefix(prefix, split, string):
    return split.join([prefix, string])

def getPrefix(string, split):
    return string.split(split)[0] 
