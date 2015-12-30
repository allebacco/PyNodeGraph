
def nodeNameFromFullname(fullname):
    """Name of the node from a fullname

    The name of the node is the first part of a fullname

    Args:
        fullname(str): Fullname of a node, connector or port

    Returns:
        The name of the node, first part of a fullname
    """
    n = fullname.split(':')[0]
    return n


def connectorNameFromFullname(fullname):
    """Name of the connector from a fullname

    The name of the connector is the second part of a fullname

    Args:
        fullname(str): Fullname of a connector or port

    Returns:
        The name of the connector, second part of a fullname or None
        if the fullname does not contains a connector
    """
    n = fullname.split(':')
    if len(n) < 2:
        return None
    return n[1]


def portNameFromFullname(fullname):
    """Name of the port from a fullname

    The name of the port is the third part of a fullname

    Args:
        fullname(str): Fullname of a port

    Returns:
        The name of the port, third part of a fullname or None
        if the fullname does not contains a port
    """
    n = fullname.split(':')
    if len(n) < 3:
        return None
    return n[2]


def getItemNames(fullname):
    """Split a fullname in the 3 parts that compose it

    Args:
        fullname(str): Fullname

    Returns:
        tuple with the names of each item in the hierarchy or None
        for the items that are not present
    """
    n = fullname.split(':')
    if len(n) == 1:
        return n[0], None, None
    if len(n) == 2:
        return n[0], n[1], None
    if len(n) == 3:
        return n[0], n[1], n[2]
    return None, None, None
