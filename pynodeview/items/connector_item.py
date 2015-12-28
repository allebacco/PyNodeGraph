import math

from PyQt4.QtCore import QRectF, QPointF
from PyQt4.QtGui import QGraphicsPathItem, QPen, QBrush, QColor, QPainterPath, QGraphicsItem

from port_item import PortItem


def anchors(count, startAngle, arcLen, radiusOut, radiusIn):
    angleIncr = arcLen / float(count + 1)
    radius = radiusIn + (radiusOut - radiusIn) / 2.0

    deg2rad = math.pi / 180.0

    points = list()
    angle = startAngle + angleIncr
    for i in xrange(count):
        x = radius * math.cos(angle*deg2rad)
        y = radius * math.sin(angle*deg2rad)
        points.append(QPointF(x, y))
        angle += angleIncr

    return points


class BaseConnectorItem(QGraphicsPathItem):

    IOTypeIn = 1
    IOTypeOut = 1 << 1

    def __init__(self, radiusOut, raiusIn, angle, arcLen, parent=None):
        QGraphicsPathItem.__init__(self, parent=parent)
        self._radiusOut = radiusOut
        self._raiusIn = raiusIn
        self._angle = angle
        self._arcLen = arcLen

        self._pen = QPen(QColor('#000000'))
        self._pen.setWidth(1)
        self.setPen(self._pen)

        self._hoverPen = QPen(QColor('#000000'))
        self._hoverPen.setWidth(2)

        brush = QBrush(QColor('#FF9966'))
        self.setBrush(brush)

        rectOut = QRectF(-radiusOut, -radiusOut, radiusOut*2.0, radiusOut*2.0)
        rectIn = QRectF(-raiusIn, -raiusIn, raiusIn*2.0, raiusIn*2.0)

        startAngle = angle - arcLen/2.0
        endAngle = angle + arcLen/2.0

        path = QPainterPath()
        path.arcMoveTo(rectIn, startAngle)
        path.arcTo(rectOut, startAngle, arcLen)
        path.arcTo(rectIn, endAngle, 0)
        path.arcTo(rectIn, endAngle, -arcLen)

        self.setPath(path)

        self._isHover = False

        self._ioDragFirstPos = None

    def ioType(self):
        return self._ioType

    def setIsHover(self, isHover):
        self._isHover = isHover
        pen = self._hoverPen if isHover else self._pen
        self.setPen(pen)
        self.update()

    def hoverEnterEvent(self, event):
        event.accept()
        self.setIsHover(True)
        QGraphicsPathItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        event.accept()
        self.setIsHover(False)
        QGraphicsPathItem.hoverLeaveEvent(self, event)


class IOConnectorItem(BaseConnectorItem):

    def __init__(self, name, portNames, angle, arcLen, ioType, parent=None):
        BaseConnectorItem.__init__(self, 50, 45, angle, arcLen, parent=parent)

        self._ioType = ioType
        self._name = name
        if parent is None:
            self._fullname = None
        else:
            self._fullname = str(self.parentItem().name()) + ':' + self._name

        self._connections = dict()
        self._ports = dict()

        connCount = len(portNames)
        startAngle = angle - arcLen / 2.0
        portPos = anchors(connCount, startAngle, arcLen, 50, 45)
        for i in xrange(connCount):
            name = portNames[i]
            port = PortItem(name, 3, parent=self)
            port.setPos(portPos[i])
            self._ports[name] = port

        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)

    def setParentItem(self, parent):
        BaseConnectorItem.setParentItem(self, parent)
        if parent is None:
            self._fullname = self._name
        else:
            self._fullname = str(self.parentItem().name()) + ':' + self._name

        for port in self._ports.itervalues():
            port.setParentFullName(self._fullname)

    def name(self):
        return self._name

    def fullname(self):
        return self._fullname

    def portNames(self):
        return self._ports.keys()

    def connections(self):
        return self._connections

    def addConnection(self, portName, conn):
        if portName in self._connections:
            return False

        self._connections[portName] = conn
        self._addConnection(portName, conn)
        return True

    def _addConnection(self, portName, conn):
        raise NotImplementedError()

    def removeConnection(self, connection):
        for name, conn in self._connections.iteritems():
            if conn == connection:
                del self._connections[name]
                return

        raise RuntimeError('%s connection is not present' % connection.name())

    def removeConnectionByPortName(self, portName):
        if portName not in self._connections:
            raise RuntimeError('%s port is not connected or present' % portName)

        del self._connections[portName]

    def removeAllConnections(self):
        self._connections = dict()

    def isConnected(self, portName):
        return portName in self._connections

    def connectionCount(self):
        return len(self._connections)

    def portCount(self):
        return len(self._ports)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.updateConnectionItems()

        return BaseConnectorItem.itemChange(self, change, value)

    def updateConnectionItems(self):
        raise NotImplementedError()


class InputConnectorItem(IOConnectorItem):

    def __init__(self, name, connectionNames, parent=None):
        IOConnectorItem.__init__(self, name, connectionNames, 180, 80, BaseConnectorItem.IOTypeIn, parent=parent)

    def updateConnectionItems(self):
        ports = self._ports
        for name, connItem in self._connections.iteritems():
            pos = ports[name].scenePos()
            connItem.setEnd(pos)

    def _addConnection(self, portName, conn):
        port = self._ports[portName]
        pos = port.scenePos()
        conn.setEnd(pos)
        conn.setEndPortName(port.fullname())


class OutputConnectorItem(IOConnectorItem):

    def __init__(self, name, connectionNames, parent=None):
        IOConnectorItem.__init__(self, name, connectionNames, 0, 80, BaseConnectorItem.IOTypeOut, parent=parent)

    def updateConnectionItems(self):
        parent = self.parentItem()
        ports = self._ports
        for name, connItem in self._connections.iteritems():
            pos = parent.mapToScene(ports[name].pos())
            connItem.setStart(pos)

    def _addConnection(self, portName, conn):
        port = self._ports[portName]
        pos = port.scenePos()
        conn.setStart(pos)
        conn.setStartPortName(port.fullname())
