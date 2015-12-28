
def nodeNameFromFullname(fullname):
    n = fullname.split(':')[0]
    return n


def connectorNameFromFullname(fullname):
    n = fullname.split(':')
    if len(n) < 2:
        return None
    return n[1]


def portNameFromFullname(fullname):
    n = fullname.split(':')
    if len(n) < 3:
        return None
    return n[2]


def getItemNames(fullname):
    n = fullname.split(':')
    if len(n) < 3:
        return None, None, None
    return n[0], n[1], n[2]
