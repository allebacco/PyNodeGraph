import math

from PyQt4.Qt import Qt
from PyQt4.QtCore import QRectF, QPointF
from PyQt4.QtGui import QGraphicsPathItem, QPen, QBrush, QColor, QPainterPath

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

        #self.setAcceptedMouseButtons(Qt.LeftButton)
        #self.setAcceptHoverEvents(True)

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

    '''
    def mousePressEvent(self, mouseEvent):
        """Manage the mouse pressing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        self._ioDragFirstPos = mouseEvent.scenePos()

    def mouseMoveEvent(self, mouseEvent):
        """Manage the mouse movement while it is pressed.

        Args:
            event(QMouseEvent): Mouse event.
        """
        if self._ioDragFirstPos is not None:
            pos = mouseEvent.scenePos()
            self.scene().ioLineDrag(self, self._ioDragFirstPos, pos, done=False)

    def mouseReleaseEvent(self, mouseEvent):
        """Manage the mouse releasing.

        Args:
            event(QMouseEvent): Mouse event.
        """
        if self._ioDragFirstPos is not None:
            pos = mouseEvent.scenePos()
            self.scene().ioLineDrag(self, self._ioDragFirstPos, pos, done=True)

        self._ioDragFirstPos = None

    def canAcceptConnection(self, fromItem):
        return self.parentItem() != fromItem.parentItem()
    '''


class IOConnectorItem(BaseConnectorItem):

    def __init__(self, connectionNames, angle, arcLen, ioType, parent=None):
        BaseConnectorItem.__init__(self, 50, 45, angle, arcLen, parent=parent)

        self._ioType = ioType
        self._name = 'in' if ioType == BaseConnectorItem.IOTypeIn else 'out'
        self._fullname = str(self.parentItem().name()) + ':' + self._name

        self._connections = dict()
        self._connectionNames = connectionNames
        self._ports = dict()

        connCount = len(self._connectionNames)
        startAngle = angle - arcLen / 2.0
        portPos = anchors(connCount, startAngle, arcLen, 50, 45)
        for i in xrange(connCount):
            name = connectionNames[i]
            port = PortItem(name, 3, parent=self)
            port.setPos(portPos[i])
            self._ports[name] = port

    def name(self):
        return self._name

    def fullname(self):
        return self._fullname

    def connectionNames(self):
        return self._connectionNames

    def connections(self):
        return self._connections

    '''
    def __getitem__(self, name):
        return self._connections[name]

    def __setitem__(self, name, connection):
        if name in self._connections:
            # remove previous connection
            self.__delitem__(name)

        self._connections[name] = connection

    def __delitem__(self, name):
        pass

    def __contains__(self, name):
        pass
    '''

    def canAcceptConnection(self, fromItem):
        ok = fromItem._ioType != self._ioType and \
             self.parentItem() != fromItem.parentItem()
        return ok


class InputConnectorItem(IOConnectorItem):

    def __init__(self, connectionNames, parent=None):
        IOConnectorItem.__init__(self, connectionNames, 180, 80, BaseConnectorItem.IOTypeIn, parent=parent)


class OutputConnectorItem(IOConnectorItem):

    def __init__(self, connectionNames, parent=None):
        IOConnectorItem.__init__(self, connectionNames, 0, 80, BaseConnectorItem.IOTypeOut, parent=parent)

